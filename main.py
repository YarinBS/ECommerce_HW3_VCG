import pandas as pd
import ex3_id1_id2 as st

data = pd.read_csv('Ex3_data.csv')

def main():
    ######### Part A ##################
    k=4
    years = list(range(2012,2017))
    # outcome = st.comb_vcg(data,k,years)

    ########## Part B ##################
    type = st.Type("vw",2015,1700,data)
    type.cars_num = 20
    type.buyers_num = 100
    # lala= type.cdf(12000)
    # print(lala)
    # type.os_cdf(80, 100, 15000)
    # print(type.avg_buy())
    print('You achieved an expected average profit of', int((type.exp_rev()/type.cars_num)-type.avg_buy()), 'per car')
    type.cars_num = 1
    type.buyers_num = 2
    print('expected revenue in a one car auction with two buyers:', type.exp_rev())
    print('Adding a median reserve price makes it', type.exp_rev_median(2))
    print('And with a third buyer that is', type.exp_rev_median(3))


if __name__ == "__main__":
    main()








