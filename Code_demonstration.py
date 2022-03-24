def to_point(x):
    try:
        return x.replace(',', '.')
    except:
        return x
    return x


def tryconvert(x):
    try:
        return x.replace(u'\xa0', '')
    except:
        return x
    return x


def to_space(x):
    try:
        return x.replace(' ', '')
    except:
        return x
    return x


name = 'C:/Users/sklyarad/Downloads/Telegram Desktop/Продажи штуки розница.csv'
with open(name, 'rb') as f:
    result = chardet.detect(f.read())

all_data = pd.read_csv(name, encoding=result['encoding'], delimiter="\t")

name = 'C:/Users/sklyarad/Downloads/Telegram Desktop/скидки розница.csv'
with open(name, 'rb') as f:
    result = chardet.detect(f.read())

pd.read_csv(name, encoding=result['encoding'], delimiter="\t")

all_data = all_data.merge(pd.read_csv(name, encoding=result['encoding'], delimiter="\t"),
                          on=['НоменклатураБезУчетаПереноса.АссортиментнаяГруппа', 'Period',
                              'НоменклатураБезУчетаПереноса.Коллекция', 'НоменклатурвБезУчетаПереносов.МесяцКоллекции'])

name = 'C:/Users/sklyarad/Downloads/Telegram Desktop/Маржа факт розница.csv'
with open(name, 'rb') as f:
    result = chardet.detect(f.read())

pd.read_csv(name, encoding=result['encoding'], delimiter="\t")

all_data = all_data.merge(pd.read_csv(name, encoding=result['encoding'], delimiter="\t"),
                          on=['НоменклатураБезУчетаПереноса.АссортиментнаяГруппа', 'Period',
                              'НоменклатураБезУчетаПереноса.Коллекция', 'НоменклатурвБезУчетаПереносов.МесяцКоллекции'])

all_data = all_data.rename(columns=lambda col: col.replace("Unnamed: 4", "Кол-во продаж"))
all_data = all_data.rename(columns=lambda col: col.replace("Unnamed: 5", "Скидка"))
all_data.rename(columns={'Кол-во продаж_x': 'Кол-во продаж', 'Кол-во продаж_y': 'Маржа'}, inplace=True)

all_data.fillna(0, inplace=True)
all_data.Скидка = all_data.Скидка.apply(lambda x: to_point(x))
all_data.Скидка = all_data.Скидка.apply(lambda x: tryconvert(x))

all_data['Кол-во продаж'] = all_data['Кол-во продаж'].apply(lambda x: to_point(x))
all_data['Кол-во продаж'] = all_data['Кол-во продаж'].apply(lambda x: tryconvert(x))
all_data['Кол-во продаж'] = all_data['Кол-во продаж'].apply(lambda x: to_space(x))
all_data['Маржа'] = all_data['Маржа'].apply(lambda x: to_point(x))
all_data['Маржа'] = all_data['Маржа'].apply(lambda x: tryconvert(x))
all_data['Маржа'] = all_data['Маржа'].apply(lambda x: to_space(x))

all_data.Скидка = pd.to_numeric(all_data.Скидка)
all_data['Кол-во продаж'] = pd.to_numeric(all_data['Кол-во продаж'])
all_data['Маржа'] = pd.to_numeric(all_data['Маржа'])
all_data = all_data[all_data.Город_наименование == "Санкт-Петербург"]
all_data = all_data.drop(['Город_наименование'], axis=1)
all_data = all_data[all_data['НоменклатураБезУчетаПереноса.АссортиментнаяГруппа'] == 'брюки']
all_data = all_data.drop(['НоменклатураБезУчетаПереноса.АссортиментнаяГруппа', 'НоменклатураБезУчетаПереноса.Коллекция',
                          'НоменклатурвБезУчетаПереносов.МесяцКоллекции'], axis=1)
all_data = all_data.groupby('Period').sum()
all_data.Скидка = all_data.Скидка / all_data['Кол-во продаж']
all_data = all_data.reset_index()
all_data['Period'] = all_data['Period'].apply(lambda x: datetime.strptime(x, '%d.%m.%Y'))
all_data = all_data.sort_values(by='Period')
all_data = all_data.set_index('Period')
Wether = pd.read_excel('C:/Storage/Data/all.xlsx', engine='openpyxl')
Wether = Wether.drop(['Атмосферное'], axis=1)
Wether = Wether.dropna(how='any', axis=0)
Wether['Дата'] = Wether['Дата'].apply(lambda x: datetime.strptime(x, '%d.%m.%Y'))
Wether['Месяц'] = Wether['Дата'].apply(lambda x: x.month)
Wether['неделя'] = Wether['Дата'].apply(lambda x: x.weekday())

start_date = DT.datetime(2019, 1, 1)
end_date = DT.datetime(2021, 12, 31)
res = pd.date_range(start_date, end_date).strftime('%d.%m.%Y').tolist()
tab = pd.DataFrame({'Дата': res, 'holiday': 0})
tab = tab.set_index('Дата')

table = pd.read_csv('C:/Storage/Data/calendar (1).csv')
col = table.columns
table = table.drop([col[0], *col[13:]], axis=1)
counter = 1
for columns in table:
    arr = table[columns].apply(lambda x: x.replace('*', '').replace('+', ''))[0].split(',')
    for i in arr:
        tab.loc[DT.datetime(2020, counter, int(i)).strftime('%d.%m.%Y')] = 1
    counter += 1

table = pd.read_csv('C:/Storage/Data/calendar (2).csv')
col = table.columns
table = table.drop([col[0], *col[13:]], axis=1)
counter = 1
for columns in table:
    arr = table[columns].apply(lambda x: x.replace('*', '').replace('+', ''))[0].split(',')
    for i in arr:
        tab.loc[DT.datetime(2019, counter, int(i)).strftime('%d.%m.%Y')] = 1
    counter += 1

table = pd.read_csv('C:/Storage/Data/calendar.csv')
col = table.columns
table = table.drop([col[0], *col[13:]], axis=1)
counter = 1
for columns in table:
    arr = table[columns].apply(lambda x: x.replace('*', '').replace('+', ''))[0].split(',')
    for i in arr:
        tab.loc[DT.datetime(2021, counter, int(i)).strftime('%d.%m.%Y')] = 1
    counter += 1
tab = tab.reset_index()
tab['Дата'] = tab['Дата'].apply(lambda x: datetime.strptime(x, '%d.%m.%Y'))
Wether = Wether.merge(tab)
Wether = Wether.set_index('Дата')

together = all_data.join(Wether)
together = together.dropna(how='any', axis=0)
together_mod_2019 = together.copy()
for i in together.columns[2:8]:
    for y in range(1, 15):
        together_mod_2019[i] += together[i].shift(y)
    for y in range(-7, 0):
        together_mod_2019[i] += together[i].shift(y)

together_mod_2019 = together_mod_2019.reset_index()
together_mod_2019 = together_mod_2019.set_index('Period')
together_mod_2019 = together_mod_2019.dropna(how='any', axis=0)

together_mod = together_mod_2019
together_mod = together_mod.reset_index()
week = together_mod['неделя']

for i in range(len(week)):
    if (week[i] == 0):
        week[i] = 7

true_num = [0] * len(week)

for i in range(len(week)):
    if (week[i] == 1):
        for y in range(1, 7):
            if i + y >= len(week):
                flag = 1
                break
            if (week[i + y] != y + 1):
                flag = 1
                break

together_mod = together_mod.set_index('Period')

together_mod['внимание'] = together_mod['неделя'].apply(lambda x: 1 if x == 0 or x == 6 else 0)

mod_dummies = pd.get_dummies(data=together_mod, columns=['Месяц', 'неделя'])
scaler = MinMaxScaler()
mod_dummies[mod_dummies.columns[1:]] = scaler.fit_transform(mod_dummies[mod_dummies.columns[1:]])
scaled = scaler.fit_transform(mod_dummies)

days_for_testing = 105
true_res = []
pred_res = []


def split_dataset(data):
    train, test = data[len(data) % 7:-days_for_testing], data[-days_for_testing:]

    test = array(split(test, len(test) / 7))

    train = array(split(train, len(train) / 7))
    return train, test


def mse_rmse(actual, predicted):
    scores = []
    for i in range(actual.shape[1]):
        mse = mean_squared_error(actual[:, i], predicted[:, i])
        rmse = sqrt(mse)
        scores.append(rmse)
    s = 0
    for row in range(actual.shape[0]):
        for column in range(actual.shape[1]):
            s += (actual[row, column] - predicted[row, column]) ** 2
    score = sqrt(s / (actual.shape[0] * actual.shape[1]))
    return score, scores


def summarize_scores(name, score, scores):
    s_scores = ', '.join(['%.1f' % s for s in scores])
    print('%s: [%.3f] %s' % (name, score, s_scores))


def prepare_to_weeks(train, to_input):
    flat_data = train.reshape((train.shape[0] * train.shape[1], train.shape[2]))
    X, y = [], []
    start = 0
    for _ in range(len(flat_data)):
        to_end = start + to_input
        out_end = to_end + 7
        if out_end <= len(flat_data):
            X.append(flat_data[start:to_end, :])
            y.append(flat_data[to_end:out_end, 0])
        start += 1
    return array(X), array(y)


def build_model(train, input_of_days):
    X_train, y_train = prepare_to_weeks(train, input_of_days)
    verbose, epochs = 1, 25
    timesteps, features, outputs = X_train.shape[1], X_train.shape[2], y_train.shape[1]
    # [samples, timesteps, features]
    y_train = y_train.reshape((y_train.shape[0], y_train.shape[1], 1))
    model = Sequential()
    model.add(LSTM(500, activation='relu', input_shape=(timesteps, features)))
    model.add(RepeatVector(outputs))
    model.add(LSTM(500, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(500, activation='relu')))
    model.add(TimeDistributed(Dense(1000, activation='relu')))
    model.add(TimeDistributed(Dense(1)))
    model.compile(loss='mse', optimizer='adam')
    print(model.fit(X_train, y_train, epochs=epochs, verbose=verbose))
    return model


def predict(model, history, input_of_days):
    data = array(history)
    data = data.reshape((data.shape[0] * data.shape[1], data.shape[2]))
    input_n_days = data[-input_of_days:, :]
    # to [1, to_input, n]
    input_n_days = input_n_days.reshape((1, input_n_days.shape[0], input_n_days.shape[1]))
    result_of_pred = model.predict(input_n_days, verbose=0)
    return result_of_pred[0]


def create_model(train, test, input_of_days):
    model = build_model(train, input_of_days)
    history = [x for x in train]
    predictions = []
    for i in range(len(test)):
        result_of_pred = predict(model, history, input_of_days)
        predictions.append(result_of_pred)
        history.append(test[i, :])
    predictions = array(predictions)
    score, scores = mse_rmse(test[:, :, 0], predictions)
    pred_res = predictions.reshape(predictions.shape[0] * predictions.shape[1])
    true_res = test[:, :, 0].reshape(test.shape[0] * test.shape[1])
    return score, scores, true_res, pred_res, model


train, test = split_dataset(scaled)

input_of_days = 21

score, scores, true_res, pred_res, model1 = create_model(train, test, input_of_days)

summarize_scores('lstm', score, scores)

scal = scaled[-len(true_res):]
scal[:, 0] = true_res
true_res = scaler.inverse_transform(scal)[:, 0]
scal = scaled[-len(true_res):]
scal[:, 0] = pred_res
pred_res = scaler.inverse_transform(scal)[:, 0]

pyplot.plot(range(105), true_res[:105], marker='o', label='true')
pyplot.plot(range(105), pred_res[:105], marker='o', label='predicted')
pyplot.legend()
pyplot.show()