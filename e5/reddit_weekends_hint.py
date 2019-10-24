import sys


OUTPUT_TEMPLATE = (
    "Initial (invalid) T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann–Whitney U-test p-value: {utest_p:.3g}"
)

def yearWeek(x):
    yWTuple = x.isocalendar()
    return yWTuple[0], yWTuple[1]

def main():
    reddit_counts = sys.argv[1]

    counts = pd.read_json(sys.argv[1], lines=True)
    counts['day'] = counts['date'].dt.dayofweek
    counts = counts[counts['subreddit'] == 'canada']
    counts = counts.loc[(counts['date'] >= '2012-01-01') & (counts['date'] <= '2013-12-31')]
    weekday = counts[counts['day'] <= 4]
    weekend = counts[counts['day'] > 4]

    ttest = stats.ttest_ind(weekday['comment_count'], weekend['comment_count']).pvalue
    normality_weekday = stats.normaltest(weekday['comment_count']).pvalue
    normality_weekend = stats.normaltest(weekend['comment_count']).pvalue
    levene = stats.levene(weekday['comment_count'], weekend['comment_count']).pvalue

    sqrtWKD = np.sqrt(weekday['comment_count'])
    sqrtWKN = np.sqrt(weekend['comment_count'])
    normality_sqrt_weekday = stats.normaltest(sqrtWKD).pvalue
    normality_sqrt_weekend = stats.normaltest(sqrtWKN).pvalue
    sqrtLevene = stats.levene(sqrtWKD, sqrtWKN).pvalue



    weekPairWkd = weekday['date'].apply(yearWeek)
    weekPairWknd = weekend['date'].apply(yearWeek)

    weekday['weekNumber'] = weekPairWkd
    weekend['weekNumber'] = weekPairWknd
    cltWKD = weekday.groupby('weekNumber').aggregate('mean')
    cltWKND = weekend.groupby('weekNumber').aggregate('mean')

    CLTttest = stats.ttest_ind(cltWKD['comment_count'], cltWKND['comment_count']).pvalue
    CLTnormality_weekday = stats.normaltest(cltWKD['comment_count']).pvalue
    CLTnormality_weekend = stats.normaltest(cltWKND['comment_count']).pvalue
    CLTlevene = stats.levene(cltWKD['comment_count'], cltWKND['comment_count']).pvalue


    mannWhitney = stats.mannwhitneyu(weekday['comment_count'], weekend['comment_count']).pvalue



    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=ttest,
        initial_weekday_normality_p=normality_weekday,
        initial_weekend_normality_p=normality_weekend,
        initial_levene_p=levene,
        transformed_weekday_normality_p=normality_sqrt_weekday,
        transformed_weekend_normality_p=normality_sqrt_weekend,
        transformed_levene_p=sqrtLevene,
        weekly_weekday_normality_p=CLTnormality_weekday,
        weekly_weekend_normality_p=CLTnormality_weekend,
        weekly_levene_p=CLTlevene,
        weekly_ttest_p=CLTttest,
        utest_p=mannWhitney,
    ))


if __name__ == '__main__':
    main()
