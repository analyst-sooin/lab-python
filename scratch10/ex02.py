import pandas as pd
import cx_Oracle
from scratch09.ex10 import get_column_names_of
from scratch09.ex10 import select_all_from
import csv


def peak_to_peak(x):
    return x.max() - x.min()






if __name__ == '__main__':
    # with - as 구문을 사용해서 오라클 DB서버에 접속
        # with-as 구문을 사용해서 Cursor 객체를 생성
            # scratch 09 패키지에서 작성한 테이블 전체 검색 함수를 사용해서,
            # emp_df, dept_df 데이터 프레임을 생성
    dsn = cx_Oracle.makedsn('localhost', 1521, 'orcl')
    with cx_Oracle.connect('scott','tiger',dsn) as connection:
        with connection.cursor() as cursor:
            emp_columns = get_column_names_of('emp',cursor)
            emp_df = select_all_from('emp',cursor)
            dept_df = select_all_from('DEPT',cursor)
            # emp_df를 csv 파일로 저장
            emp_df.to_csv('emp_df.csv')
            # emp_df 에서 부서별 평균 급여를 출력( groupby 를 deptno)
            group_deptno = emp_df.groupby('DEPTNO')
            sal_by_dept = group_deptno['SAL']
            gp_deptno_mean_sal = group_deptno['SAL'].mean()
            print(gp_deptno_mean_sal)

            # emp_df 에서 부서별 인원수를 출력
            gp_deptno_cnt = group_deptno['ENAME'].count()
            print(gp_deptno_cnt)

            # emp_df에서 부서별 급여 최소값 출력
            gp_deptno_sal_min = group_deptno['SAL'].min()
            print(gp_deptno_sal_min)

            # emp_df에서 부서별 급여 최대값 출력
            gp_deptno_sal_max = group_deptno['SAL'].max()
            print(gp_deptno_sal_max)

            # 위에 결과를 하나의 데이터 프레임으로 출력
            df =pd.DataFrame({
                'count' :  gp_deptno_cnt,
                'mean' : gp_deptno_mean_sal,
                'min' : gp_deptno_sal_min,
                'max' : gp_deptno_sal_max
            })
            print(df)

            #agg(), aggregate() :파라미터에 함수 이름( 또는 리스트)를 전달하면
            # GroupBy 객체에 함수를 적용한다
            # 함수가 집계 함수(pandas.Series 또는 pandas.DataFrame 클래스가
            # 가지고 있는 메소드들 :count, mean, sum,...)인 경우에는 함수이름을 문자열로 전달함.
            # 개발자가 작성한 함수는 함수이름을 파라미터로 전달해야함

            df = sal_by_dept.agg(['count','mean','min','max',peak_to_peak])
            print(df)


            # emp_df에서 직책별 직원 수, 급여 평균 최소,최대 값을 출력
            grouped_by_job= emp_df.groupby('JOB')
            sal_by_job = grouped_by_job['SAL']
            print(sal_by_job.agg(['count','mean','min','max',
                                  lambda x: x.max() - x.min()]))
            # agg() 함수가 만드는 DataFrame의 컬럼 이름을 설정할때는
            # keyword-arguement 방식 또는 dict를 파라미터로 전달함.
            print( sal_by_job.agg(Count = 'count',
                                  Average = 'mean',
                                  Minimum = 'min',
                                  Maximum = 'max',
                                  Range = lambda x : x.max()- x.min()))

            # emp_df에서 부서별, 직책별 직원 수 ,급여평균, 최소,최대 값 출력
            grouped = emp_df.groupby(['DEPTNO','JOB'])
            sal_by_dept_job = grouped['SAL']
            df = sal_by_dept_job.agg({
                'count': 'count',
                'minimum' : 'min',
                'maximum' : 'max',
                'average' : 'mean',
                'range': lambda x: x.max() - x.min()
            })
            # agg(), aggregate() 함수의 파라미터에 dict를 전달하는 방식은
            # pandas 패키지가 업그레이될 떄 없어질수 있는 기능(deprecated)
            # dict 방식보다는 keyword - arguement 방식을 사용하는 것이 안전함.
            
            print(df)




