import sys
import pandas as pd
from scipy import stats

OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value: {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value: {more_searches_p:.3g}\n'
    '"Did more/less instructors use the search feature?" p-value: {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value: {more_instr_searches_p:.3g}'
)
def count(df):
    searched = df.loc[df['search_count'] > 0].count()[2]
    not_searched= df.loc[df['search_count'] <= 0].count()[2]
    return searched, not_searched

def getValues(search_data):
    new_design_user = search_data.loc[search_data['uid'] % 2 == 1]
    old_design_user = search_data.loc[search_data['uid'] % 2 == 0]

    new_searched, new_not_searched = count(new_design_user)
    old_searched, old_not_searched = count(old_design_user)

    allUsers_contingency = pd.DataFrame(
    [[new_searched, new_not_searched],[old_searched, old_not_searched]],
     columns=['Searched', 'Not Searched'],
     index=pd.Index(['New Desing Searches Count','Old Design Searches Count']))

    g, p, dof, expctd = stats.chi2_contingency(allUsers_contingency)
    searches_p = stats.mannwhitneyu(new_design_user['search_count'], old_design_user['search_count']).pvalue

    return p, searches_p


def main():
    searchdata_file = sys.argv[1]

    search_data = pd.read_json(searchdata_file, orient='records', lines=True)
    instructor_data = search_data.loc[search_data['is_instructor'] == True]
    more_p, more_searches_p = getValues(search_data)
    more_instr_p, more_instr_searches_p = getValues(instructor_data)


    print(OUTPUT_TEMPLATE.format(
        more_users_p=more_p,
        more_searches_p=more_searches_p,
        more_instr_p=more_instr_p,
        more_instr_searches_p=more_instr_searches_p,
    ))




if __name__ == '__main__':
    main()
