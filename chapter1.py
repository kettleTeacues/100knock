import pandas as pd
import matplotlib.pyplot as plt

# 素データ取得
custMaster = pd.read_csv('100knock-data_analytics/1章/customer_master.csv')
itemMaster = pd.read_csv('100knock-data_analytics/1章/item_master.csv')
tran1 = pd.read_csv('100knock-data_analytics/1章/transaction_1.csv')
tran2 = pd.read_csv('100knock-data_analytics/1章/transaction_2.csv')
td1 = pd.read_csv('100knock-data_analytics/1章/transaction_detail_1.csv')
td2 = pd.read_csv('100knock-data_analytics/1章/transaction_detail_2.csv')

# 連結
transaction = pd.concat([tran1, tran2], ignore_index=True)
transactionDetail = pd.concat([td1, td2], ignore_index=True)

# マージ
mergeDF = transactionDetail.merge(transaction, on='transaction_id', how='left')
mergeDF = mergeDF.merge(custMaster, on='customer_id', how='left')
mergeDF = mergeDF.merge(itemMaster, on='item_id', how='left')

# transactionDetailごとの取引金額を算出
mergeDF['transPrice'] = mergeDF.quantity * mergeDF.item_price

# 統計
def statistic():
    print(mergeDF.isnull().sum())
    print(f'\n\n{mergeDF.payment_date.min()} - {mergeDF.payment_date.max()}')
    print(mergeDF.describe())

# ノック8：月別データ分析
# 月ごとにグルーピングした金額の集計
def knock8():
    mergeDF.payment_date = pd.to_datetime(mergeDF.payment_date) # 文字列を日付型に変換
    mergeDF['paymentMonth'] = mergeDF.payment_date.dt.strftime('%Y%m') # 日付型に対してdt(列一括処理)アクセサを使って文字列フォーマットを適用
    # print(mergeDF.groupby('paymentMonth').sum(numeric_only=True).price) # 月ごとにグルーピングして合計した金額を取得

# ノック9：月別商品別分析
def knock9():
    # 月商品ごとにグルーピングして金額と数量を取得
    print(mergeDF.groupby(['paymentMonth', 'item_name']).sum(numeric_only=True)[['price', 'quantity']])

    # ↑と同じことをピボットテーブルで行う
    print(
        pd.pivot_table(
            mergeDF,
            index='item_name',
            columns='paymentMonth',
            values=['price', 'quantity'],
            aggfunc='sum'
        )
    )

# ノック10：ピボットテーブルをグラフ化
def knock10():
    knock8()
    graphData = pd.pivot_table(
        mergeDF,
        index='paymentMonth',
        columns='item_name',
        values='price',
        aggfunc='sum'
    )
    print(graphData)

    plt.plot(list(graphData.index), graphData['PC-A'], label='PC-A')
    plt.plot(list(graphData.index), graphData['PC-B'], label='PC-B')
    plt.plot(list(graphData.index), graphData['PC-C'], label='PC-C')
    plt.plot(list(graphData.index), graphData['PC-D'], label='PC-D')
    plt.plot(list(graphData.index), graphData['PC-E'], label='PC-E')
    plt.legend()
    plt.show()

knock10()