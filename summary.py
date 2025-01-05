import pandas as pd
import sys

def CalcDeviationRank(rank):
    # To calcurate deviation of rank
    return abs(4 - rank)

def CalculateScore(scorefile):
    average_score = scorefile['score'].mean()
    average_rank = scorefile['rank'].mean()
    average_rank = CalcDeviationRank(average_rank)

    for ply in scorefile.groupby('player'):
        p_avg_score, p_avg_rank = ply[1][['score', 'rank']].mean()
        p_max = ply[1]['score'].max()

        # To calcurate deviation of rank
        p_avg_rank_abs = CalcDeviationRank(p_avg_rank)

        # T-score
        TScore_s = (p_avg_score - average_score) /scorefile['score'].std() * 10 + 50
        TScore_r = (p_avg_rank_abs - average_rank) / scorefile['rank'].std() * 10 + 50
        TScore = (TScore_s + TScore_r) / 2

        # Round
        p_average = round(p_avg_score, 2)
        p_rank = round(p_avg_rank, 2)
        p_max = round(p_max, 2)
        TScore = round(TScore, 2)

        print(f'{ply[0]}')
        print(f'    対局数: {len(ply[1])}')
        print(f'    平均スコア: {p_average}')
        print(f'    最高スコア: {p_max}')
        print(f'    平均順位  : {p_rank}')
        print(f'    スコア&ランク偏差値: {TScore}')


def main():
    ScoreFlag = None

    if len(sys.argv) <= 1:
        print('Usage: python summary.py <filename> <option>')
        sys.exit(1)
    elif len(sys.argv) == 2:
        pass
    elif len(sys.argv) == 3:
        if sys.argv[2] == '--hansou' or sys.argv[2] == '--tonpu':
            ScoreFlag = sys.argv[2]
        else:
            print('Usage: option is --hansou or --tanou')
    else:
        print('Usage: option is --hansou or --tanou')
        sys.exit(1)

    FileName = sys.argv[1]

    mj_df = pd.read_csv(FileName)
    hansou_df = mj_df[mj_df['gameid'].str.contains('H')]
    tonpu_df = mj_df[mj_df['gameid'].str.contains('T')]

    if len(sys.argv) == 2:
        print('=====  総合スコア  =====')
        CalculateScore(mj_df)
        print('=====  半荘戦スコア  =====')
        CalculateScore(hansou_df)
        print('=====  東風戦スコア  =====')
        CalculateScore(tonpu_df)
    elif ScoreFlag is not None and ScoreFlag == '--hansou':
        print('=====  半荘戦スコア  =====')
        CalculateScore(hansou_df)
    elif ScoreFlag is not None and ScoreFlag == '--tonpu':
        print('=====  東風戦スコア  =====')
        CalculateScore(tonpu_df)

if __name__ == '__main__':
    main()
