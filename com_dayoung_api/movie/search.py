# 네이버 검색 API예제는 블로그를 비롯 전문자료까지 호출방법이 동일하므로 blog검색만 대표로 예제를 올렸습니다.
# 네이버 검색 Open API 예제 - 블로그 검색
import os
import sys
import urllib.request
import json
import csv
import pandas as pd
from pandas import DataFrame

from pathlib import Path
from com_dayoung_api.utils.file_helper import FileReader

'''
10/23 rev1.0
5가지 추가 필요
중복 데이터의 제거 기능
    - 제목, 년도, 감독 의 값이 동일하면 df에서 제거 (csv는 유지? )
null 값의 대체 입력 기능
    - ui 단에서 사진이 짤려서 나와서 사진 크기에 영향 줌
정리하고 주석 달기 
    - 파일 변경 같은 부분(주석 달린 부분) filehelper로 옮기기
merge_df 단에서 네이버 영화 df를 읽어오지 말고 csv로 읽어오기?
    - 항상 api를 검색하면 시간이 오래걸림 csv를 만들고 df로 읽어오게 변환
검색 정확도 높이기
    - 특수 문자, 한자 등 제거 하여 검색 정확도 높이기?
    - 검색 안되는 값이 주로 옜날 영화이니 year컬럼 기준으로 index삭제 하기 (ex 1980 이전은 삭제)
검색 delay 주기
    - 검색시에 데이터가 너무 많고, 집에 인터넷이 느린지 에러가 발생
    - c 언어 처럼 delay를 줄 수 있는지 찾아 보기
bit pj api로 옮기기 (파일명 search ??)
    - bit pj로 옮기고 실행 마무리 하기 (최종 단계) / git api 아이디 비번 삭제!
'''

class NaverMovie:
    def __init__(self):
        self.fileReader = FileReader()  
        self.path = os.path.abspath("")
        self.client_id = "FbBHL08d_rByl4JUGuNa"                         # 네이버 api id (git 삭제!!!)
        self.client_secret = "7HoTkF84oJ"                               # 네이버 api secret (git 삭제!!!)

    def hook(self):
        print('*'*10, 'START', '*'*10)
        
        kmdb_df = self.read_kmdb_csv()                                  # step1 : kmdb_csv 읽어와서 df으로 전환 (return : df)
        kmdb_movie_title_list = self.get_title_list(kmdb_df)            # step2 : 검색을 위한 제목 list 추출 (return : list)
        kmdb_movie_year_list = self.get_year_list(kmdb_df)              # step3 : 검색을 위한 년도 list 추출 (return : list)

        print('*'*30)

        movie_dict = self.search_naver_movie(kmdb_movie_title_list,\
                                                kmdb_movie_year_list)   # step4 : 네이버 영화 api 검색 진행 (return : dict)
        naver_movie_df = self.dict_to_dataframe(movie_dict)             # step5 : 네이버 영화 검색 dict df 전환 및 csv 저장 (return : df)
        merge_df = self.merge_df(kmdb_df, naver_movie_df)               # step6 : ui json 생성을 위한 kmdb_csv(df)와 네이버 영화 검색(df) merge (retrun : df)
        ui_df = self.df_to_ui_json(merge_df)                                    # step7 : merge_df의 column 삭제 및 정렬 후 json파일 저장
        return ui_df
        print('*'*10, 'E N D', '*'*10)

    def read_kmdb_csv(self):
        path = os.path.abspath("")
        fname = '\data\kmdb_csv.csv'
        kmdb_df = pd.read_csv(path + fname, encoding='euc_kr')
        return kmdb_df

    def get_title_list(self, data):
        kmdb_movie_title_list = []
        for i in data['title']:
            kmdb_movie_title_list.append(i)

        return kmdb_movie_title_list

    def get_year_list(self, data):
        kmdb_movie_year_list = []
        for i in data['year']:
            kmdb_movie_year_list.append(i)

        return kmdb_movie_year_list

    def search_naver_movie(self, kmdb_movie_title_list, kmdb_movie_year_list):
        titlelist = []    # kmdb의 영화 이름이 저장될 list
        yearlist = []     # kmdb의 영화 년도가 저장될 list
        real_dict = {}    # 네이버영화의 json값을 저장할 dict
        movie_index = 0   # kmdb csv의 인덱스
        ui_json_id = 100  # ui_json의 인덱스    
        print('검색 시작!!!!!!!!!!!!!!!!!')

        for kmdb_year in kmdb_movie_year_list:
            yearlist.append(kmdb_year)

        for kmdb_title in kmdb_movie_title_list:    # kmdb title로 naver title 검색
            titlelist.append(kmdb_title)
            print('*'*30)           
            print(f'영화 인덱스 : {movie_index}번')
            print(f'검색 제  목 : {kmdb_title}') # 검색 영화 제목
            print(f'검색 연  도 : {yearlist[movie_index]}') # 검색 영화 연도

            encText = urllib.parse.quote(kmdb_title)
            display = "&display=100"
            yearfrom = (f"&yearfrom={yearlist[movie_index]}")
            yearto = (f"&yearto={yearlist[movie_index]}")
            url = "https://openapi.naver.com/v1/search/movie.json?query=" \
                                                                            + encText \
                                                                            + display \
                                                                            + yearfrom \
                                                                            + yearto
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",self.client_id)
            request.add_header("X-Naver-Client-Secret",self.client_secret)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
            
            if(rescode==200):
                response_body = response.read().decode('utf-8')
                jsondata = json.loads(response_body)
                items = jsondata['items']
                temp_dict = {}
                
                if items == []: # kmdb의 영화제목이 네이버 영화에 없는 경우
                    real_data = {'title':'none',
                                'link':'none',
                                'image':'../images/none_image.jpg',
                                'subtitle':'none',
                                'pubDate':'none',
                                'director':'none',
                                'actor':'none',
                                'userRating':'0',
                                'id':ui_json_id}                                    
                    temp_dict[movie_index] = real_data
                    real_dict.update(temp_dict)

                else:           # kmdb의 영화제목이 네이버 영화에 있는 경우
                    i = 0
                    
                    for i in range(len(items)):    # dict에 네이버 영화 정보 추가
                        titles = items[i]['title']
                        titles_drop1 = titles.replace('<b>', '').replace('</b>', '')  # <b>, </b>삭제
                        titles_drop2 = titles_drop1.replace(' ', '')                  # 공백 제거
                        images = items[i]['image']
                        titlelist_drop1 = titlelist[movie_index].replace(' ', '')     # kmdb제목 공백 제거
                        real_data = []
                        
                        '''
                        case0: kmdb의 영화 제목이 네이버에 없는 경우
                        case1: 영화 image 없음, 제목 일  치 (공백 포함)
                        case2: 영화 image 없음, 제목 일  치 (공백 제거)
                        case3: 영화 image 없음, 제목 불일치
                        case4: 영화 image 있음, 제목 일  치 (공백 포함)
                        case5: 영화 image 있음, 제목 일  치 (공백 제거)
                        case6: 영화 image 있음, 제목 불일치
                        '''

                        if images == "":                                                 # 네이버에 영화 image가 없는 경우
                            if titles_drop1 == titlelist[movie_index]:                   # kmdb제목과 naver 제목(drop1) 일치 확인
                                real_data = items[i]                                     # naver 영화 json의 value값 저장
                                real_data['image'] = '../images/none_image.jpg'          # none_image.jpg로 표시
                                userrating_naver = float(real_data['userRating'])/2      # 별점 10점 만점 -> 5점 만점
                                userrating_naver = '%0.1f' % float(userrating_naver)
                                real_data['userRating'] = userrating_naver              
                                real_data['id'] = ui_json_id                             # ui의 image card 인덱스 값
                                temp_dict[movie_index] = real_data                       # {kmdb의 title값 : naver영화 json value}
                                real_dict.update(temp_dict)
                                print('case1')
                            elif titles_drop2 == titlelist_drop1:                        # kmdb제목과 naver 제목(drop2) 일치 확인
                                real_data = items[i]                                     
                                real_data['image'] = '../images/none_image.jpg'                    
                                userrating_naver = float(real_data['userRating'])/2      
                                userrating_naver = '%0.1f' % float(userrating_naver)
                                real_data['userRating'] = userrating_naver              
                                real_data['id'] = ui_json_id                             
                                temp_dict[movie_index] = real_data                       
                                real_dict.update(temp_dict)
                                print('case2')
                            else:
                                real_data = items[i]                                     
                                real_data['image'] = '../images/none_image.jpg'                    
                                userrating_naver = float(real_data['userRating'])/2      
                                userrating_naver = '%0.1f' % float(userrating_naver)
                                real_data['userRating'] = userrating_naver              
                                real_data['id'] = ui_json_id                             
                                temp_dict[movie_index] = real_data                       
                                real_dict.update(temp_dict)
                                print('case3')
                        else:                                                            # 네이버에 영화 image가 없는 경우
                            if titles_drop1 == titlelist[movie_index]:               
                                real_data = items[i]                                    
                                userrating_naver = float(real_data['userRating'])/2  
                                userrating_naver = '%0.1f' % float(userrating_naver)
                                real_data['userRating'] = userrating_naver              
                                real_data['id'] = ui_json_id                           
                                temp_dict[movie_index] = real_data                       
                                real_dict.update(temp_dict)
                                print('case4')
                            elif titles_drop2 == titlelist_drop1:                 
                                real_data = items[i]                                     
                                userrating_naver = float(real_data['userRating'])/2      
                                userrating_naver = '%0.1f' % float(userrating_naver)
                                real_data['userRating'] = userrating_naver              
                                real_data['id'] = ui_json_id                             
                                temp_dict[movie_index] = real_data                       
                                real_dict.update(temp_dict)
                                print('case5')
                            else:
                                real_data = items[i]                                     
                                userrating_naver = float(real_data['userRating'])/2      
                                userrating_naver = '%0.1f' % float(userrating_naver)
                                real_data['userRating'] = userrating_naver              
                                real_data['id'] = ui_json_id                             
                                temp_dict[movie_index] = real_data                       
                                real_dict.update(temp_dict)
                                print('case6')        
                                                    
                        # if 3 end
                    i += 1
                    # inner for end
                # if 2 end
                ui_json_id += 100    
            else:
                print("Error Code:" + rescode)
            # if 1 end
            movie_index += 1
        # outter for end
        print('*'*30)
        print('검색 끝!!!!!!!!!!!!!!!!!!')
        # print(real_dict)
        return real_dict

    def dict_to_dataframe(self, movie_dict): # -> filehelper로 옮기기 / movie_dict는 전역값으로 받아오게 하기?
        print('*****to dataframe 진행*****')
        myframe = DataFrame(movie_dict)

        # title, link, image, subtitle, pubDate, director, actor, userRating
        navermovie_index = \
            {'title':'title_naver',
            'link':'link_naver',
            'image':'image_naver',
            'subtitle':'subtitle_naver',
            'pubDate':'pubdate_naver',
            'director':'director_naver',
            'actor':'actor_naver',
            'userRating':'userrating_naver'}               
        myframe = myframe.rename(index=navermovie_index)
        myframe = myframe.T
        # print(myframe)
        # myframe.to_csv('test.csv', encoding='utf-8', index=True)    # -> filehelper로 옮기기
        print('*****to dataframe 완료*****')        
        return myframe

    def merge_df(self, kmdb_df, naver_movie_df):
        print('*****df merge 진행*****')
        merge_df = pd.concat([kmdb_df, naver_movie_df],axis=1)
        # merge_df.to_csv('merge_test.csv', encoding='utf-8')   # -> filehelper로 옮기기
        # print(merge_df)
        print('*****df merge 완료*****')        
        return merge_df

    def df_to_ui_json(self, merge_df):
        print('*****to json 진행*****')

        '''
        ***** 현재 columns *****
        title,
        genre,
        country,
        year,
        company,
        director,
        actor,
        date,
        running_time,
        keyword,
        plot,
        title_naver,
        link_naver,
        image_naver,
        subtitle_naver,
        pubdate_naver,
        director_naver,
        actor_naver,
        userrating_naver
        '''
        '''
        ***** 만들 json sample *****
        {
        "id": 900,
        "title": "Resident Evil",
        "subtitle": "Vendetta",
        "description": "Chris Redfield enlists the help of Leon S. Kennedy and Rebecca Chambers to stop a death merchant, with a vengeance, from spreading a deadly virus in New York.",
        "year": 2014,
        "imageUrl": "../images/담보.jpg",
        "rating": 4.2
        }
        '''

        # 필요 없는 column drop
        drop_df = merge_df.drop \
                    (['country', 
                    'company', 
                    'director', 
                    'actor', 
                    'date', 
                    'running_time',
                    'plot', 
                    'title_naver', 
                    'link_naver',  
                    'subtitle_naver', 
                    'pubdate_naver', 
                    'director_naver', 
                    'actor_naver'], axis=1)
        
        # ui json 형식에 맞게 sorting
        sort_df = drop_df[['id', 'title', 'genre', 'keyword', 'image_naver', 'year', 'userrating_naver']]
        
        ui_json_columns = {
            'id':'movieid',
            'genre':'subtitle',
            'keyword':'description',
            'image_naver':'imageurl',
            'userrating_naver':'rating'
        }
        # ui json과 동일하게 colunm 이름 변경
        rename_df = sort_df.rename(columns=ui_json_columns)
        fill_na_df = rename_df.fillna('none')
        print(fill_na_df)
        # ui_json = DataFrame.to_json(fill_na_df, orient = 'records', force_ascii=False, indent=8)
        # print(ui_json)
        # save_json = json.loads(ui_json)                                       # --> filehelper로 옮기기
        # with open('movies.json', 'w', encoding='utf-8') as make_json:         # --> 강사님 수정 위해 json 변환 막음
        #     json.dump(save_json, make_json, ensure_ascii=False, indent="\t")  # --> 강사님 수정 위해 json 변환 막음
        print('*****to json 완료*****')
        return fill_na_df

# if __name__ == "__main__":
#     test = NaverMovie()
#     test.hook()


