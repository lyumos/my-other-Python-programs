from sklearn.model_selection import train_test_split, GridSearchCV  # sklearn для МО
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
import pandas as pd  # обработка массивов данных
import numpy as np  # тоже для обработки, удаления пропускков и прочего
import subprocess  # для вызова команд терминала из кода
import pybrologs  # библиотека для для чтения и обработки лог-файлов, созданных Bro IDS
import sklearn
import joblib  # для загрузки модели в код
import glob  # для поиска пути до файла в директории
import os  # для работы с ос


# подготовка датасета
def dataset_handler():
    df = pd.read_csv('raw_dataset.csv')

    # удаляем пустые и прочие неприятные значения
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)

    # удаляем дубликаты строк
    df.drop_duplicates(inplace=True)
    df.reset_index(inplace=True, drop=True)

    # нормализация данных
    x_norm = df.loc[:, ~df.columns.isin(['Label'])]
    scaler = MinMaxScaler()
    df_norm = pd.DataFrame(scaler.fit_transform(x_norm), columns=x_norm.columns)

    # совмещаем Label и нормализованный датафрейм
    final_df = pd.concat([df_norm, df['Label']], axis=1)

    # разделяем на тестовую и тренировочную выборки
    x = final_df.iloc[:, :-1]
    y = final_df.iloc[:, -1]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30, random_state=77, stratify=y)

    return x_train, x_test, y_train, y_test


# создание модели, прогнозирование и оценивание
def create_model(x_train, x_test, y_train, y_test):
    classifier = RandomForestClassifier()
    params = {
              'n_estimators': [50, 100, 150, 200],
              'criterion': ['gini', 'entropy'],
              'min_samples_leaf': [0.1, 0.2, 0.3, 0.4, 0.5, 1],
              'min_samples_split': [0.5, 1.0, 2, 3, 4],
              'max_features': ['sqrt', 'log2']
              }

    # выбор наилучших параметров для RF и датасета и создание модели
    model = GridSearchCV(classifier, params, cv=5)

    # обучение модели на выбранных параметрах
    model.fit(x_train, y_train)

    # прогнозирование на тестовой выборке
    y_pred = rf_model.predict(x_test)

    # вывод наилучших параметров и значений Accuracy, Recall, Precision, F-score
    print(f'Выбранные параметры: {rf_model.best_params_}')
    print(classification_report(y_test, y_pred, digits=4, labels=[0, 1], target_names=['normal', 'APT']))

    return model


# функция, где собраны 2 вышеперечисленные функции для режима обучения
def main_learning():
    # получение тренировочных и тестовых данных после обработки датасета
    x_tr, x_t, y_tr, y_t = dataset_handler()

    # создание модели
    rf_model = create_model(x_tr, x_t, y_tr, y_t)

    # сохранение модели
    with open('rf_model.pkl', 'wb') as f:
        pickle.dump(rf_model, f)


# запуск broctl и соединение с bro ids
def get_conn():
    subprocess.run(['/usr/local/bro/bin/broctl', "start"])
    # ниже можешь вставить свои данные
    connection = brologs.BroLogConnection('hostname', 47758, 'admin', 'password')
    if connection:
        print('Подключение к Bro IDS выполнено успешно!')
        return connection
    else:
        return None


# остановка broctl
def close_conn():
    subprocess.run(['/usr/local/bro/bin/broctl', "stop"])
    print('Произведена остановка Bro IDS')


# загрузка и обработка имеющихся в папке логов
def logs_handler(attributes, connection):
    logs = connection.get_logs('/usr/local/bro/logs/')

    # из каждого лога выбираем нужные признаки и записываем в общий файл
    for log in logs:
        log_path = glob.glob('/usr/local/bro/logs/' + '*.log')
        required_log = subprocess.check_output(['bro-cut', '-d', ',', attributes, log_path])
        with open('logs.csv', 'wb') as f:
            f.write(required_log)
        # удаляем старые логи, которые уже обработаны
        os.remove(os.path.join('/usr/local/bro/logs/', log))
    file = pd.read_csv('logs.csv')
    return file


# прогнозирование и создание файла логов с метками класса
def predict_labels(file, model):
    file['Label'] = None

    # прогнозирование для каждой строки и выставление метки в крайний правый столбик
    for index, row in file.iterrows():
        row_df = pd.DataFrame([row.values], columns=file.columns)
        label = int(model.predict(row_df))
        file.loc[index, 'label'] = label
    return file


# функция, где собраны 5 вышеперечисленных функций для режима прогнозирования
def main_classification():
    # признаки можно менять
    attrs = [
            'Anomaly port or protocol', 'Ratio of number of packets OUT/IN', 'Ratio of number of Bytes OUT/IN',
            'Number of three way handshakes', 'Number of connection teardowns', 'Number of complete conversation',
            'Anomaly Data', 'Number of packets per time', 'Number of bytes per time', 'Percentage of TCP SYN Packets',
            'Percentage of TCP SYN ACK Packets', 'Percentage of TCP ACK Packets', 'Percentage of TCP ACK PUSH Packets',
            'Command and File System', 'Data to computer in LAN', 'Tor Network'
    ]
    # загрузка модели
    ml_model = joblib.load('rf_model.pkl')

    conn = get_conn()
    if conn:
        decision = 'Да'
        while decision == 'Да':
            # проверка, есть ли в директории файлы с логами
            if os.path.isfile('/usr/local/bro/logs/*.log'):
                # создание сырого файла со всеми логами
                logs_file = logs_handler(attrs, conn)

                # создание лог-файла с метками
                labeled_logs_file = predict_labels(logs_file, ml_model)

                # вывод мини-статистики
                print(
                    f'Было обработано {len(labeled_logs_file)} записей, '
                    f'{int((len(df[df["label"] == 1]) / len(labeled_logs_file)) * 100)}% из них составляют аномалии'
                )
                decision = input('Требуется ли обработка новых лог-файлов? (Да/Нет) ')
            else:
                print('В директории отсутствуют лог-файлы')
                decision = 'Нет'
        close_conn()
    else:
        print(
              'Подключение к Bro IDS не выполнено. '
              'Требуется изменить настройки подключения и запустить программный модуль снова.'
              )


def mode_choice():
    mode = input('Выберите режим работы (Обучение/Прогнозирование): ')
    if mode == 'Обучение':
        main_learning()
        choice = input('Модель обучения создана и сохранена. Продолжить в режиме прогнозирования? (Да/Нет)')
        if choice == 'Да':
            mode = 'Прогозирование'
    if mode == 'Прогнозирование':
        main_classification()


if __name__ == '__main__':
    mode_choice()
