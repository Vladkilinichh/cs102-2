import requests
import time
from datetime import datetime
from config import VK_CONFIG
import plotly

cur_date = datetime.now()

config = {
    'VK_ACCESS_TOKEN': 'Tокен доступа для ВК',
    'PLOTLY_USERNAME': 'Имя пользователя Plot.ly',
    'PLOTLY_API_KEY': 'Ключ доступа Plot.ly'
}


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for i in range(max_retries):
        try:
            res = requests.get(url, params=params, timeout=timeout)
            return res
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                raise
            backoff_value = backoff_factor * (2 ** i)
            time.sleep(backoff_value)


def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    
    url = '{https://api.vk.com/method}/friends.get?user_id={pgtklddabz}&fields={fields}&access_token={9651584c93f1db85b7974eb1de1abe755ad0e70cd601990f036b5c4adec4444b595989c5137b28ff4775e}&v=5.53'
    return requests.get(url).json()['response']['items']

    params = {
        'access_token':'9651584c93f1db85b7974eb1de1abe755ad0e70cd601990f036b5c4adec4444b595989c5137b28ff4775e',
        'user_id':'pgtklddabz',
        'fields':fields,
        'domain':'https://api.vk.com/method'
    }

    
    url = '{domain}/friends.get?user_id-{user_id}&fields-{fields}&access_token-{access_token}&v-5.53'
    

    for i in range(5):
        try:
            friends = requests.get(url(url.format(**params)).json()['response']['items'])
            break
        except Exception:
            time.sleep(random.random()*3+1)

    return friends
        



def age_predict(user_id):
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    ages = []

    for item in get_friends(user_id, 'bdate'):
        try:
            d,m,y = [int(i) for i in item['bdate'].split('.')]
            age = cur_date.year - y - (m > cur_date.month or m == cur_date.month and d < cur_date.day)
            ages.append(ages)
        except KeyError:
            pass
        except ValueError:
            pass

    return (sum(ages) / len(ages))
    ages.sort()       


def messages_get_history(user_id, offset=20, count=20):
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    url = "https://api.vk.com/method/messages.getHistory"
    parameters = {
        'access_token': config.VK['VK_ACCESS_TOKEN'],
        'user_id': user_id,
        'offset': offset,
        'count': count,
        'rev': rev,
        'v': config.VK['API_VERSION']
    }
    messages_history = get(url, params=parameters)
    return messages_history


def count_dates_from_messages(messages):
    """ Получить список дат и их частот

    :param messages: список сообщений
    """
    freq_list = ([], [])
    for mes in messages:
        date = fromtimestamp(mes['date'])
        if date in freq_list[0]:
            ind = freq_list[0].index(date)
            freq_list[1][ind] += 1
        else:
            freq_list[0].append(date)
            freq_list[1].append(1)
    return freq_list


def plotly_messages_freq(freq_list):
    """ Построение графика с помощью Plot.ly

    :param freq_list: список дат и их частот
    """
    x = dates
    y = freq
    data = [go.Scatter(x=x, y=y)]
    py.plot(data)


def get_network(users_ids, as_edgelist=True):
    users_ids = get_friends(user_id, "")
    edges = []
    matrix = [[0] * len(users_ids) for i in range(len(users_ids))]

    for user1 in range(len(users_ids)):
        friends = get_friends(users_ids[user1])
        for user2 in range(user1 + 1, len(users_ids)):
            if users_ids[user2] in friends:
                if as_edgelist:
                    edges.append((user1, user2))
                else:
                    matrix[user1][user2] = 1
                    matrix[user2][user1] = 1
        time.sleep(0.4)

    if as_edgelist:
        return edges
    return matrix


def plot_graph(graph):
    surnames = get_friends(user_id, 'last_name')
    vertices = [i['last_name'] for i in surnames]
    edges = get_network(user_id, True)

    draf = igraph.Graph(vertex_attrs={"shape": "circle", "label": vertices, "size": 10},
                     edges=edges, directed=False)

    n = len(vertices)
    visual_style = {
        "vertex_size": 20,
        "edge_color": "gray",
        "layout": draf.layout_fruchterman_reingold(
            maxiter=100000,
            area=n ** 2,
            repulserad=n ** 2)
    }

    draf.simplify(multiple=True, loops=True)
    clusters = draf.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    draf.vs['color'] = pal.get_many(clusters.membership)
    igraph.plot(draf, **visual_style)
