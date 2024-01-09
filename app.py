import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests


def recommend(book_name):
    recommended_books = []
    recommended_poster = []
    index = np.where(pt.index== book_name)[0][0]
    similar = sorted(list(enumerate(similarity_scores[index])), key = lambda x :x[1],reverse = True)[1:11]
    for i,j in similar:
        recommended_books.append(pt.index[i])
    for book in recommended_books:
        unique_df = books.drop_duplicates(subset = 'Book-Title')
        poster = unique_df[unique_df['Book-Title'] == book]['Image-URL-L'].values[0]
        recommended_poster.append(poster)
    return recommended_books,recommended_poster

book_dict = pickle.load(open('books_dict.pkl','rb'))
books = pd.DataFrame(book_dict)
popular_dict = pickle.load(open('popular.pkl','rb'))
popular_df = pd.DataFrame(popular_dict)
similarity_scores = pickle.load(open('similarity.pkl','rb'))
pt = books.pivot_table(index ='Book-Title',columns='User-ID',values = 'Book-Rating')
pt.fillna(0,inplace = True)


st.sidebar.title("Book Recommender")
user_menu = st.sidebar.radio(
    '-------------',
    ('Home Page', 'Recommender System','About the Recommender System' )
)

if user_menu == 'Home Page':
    st.title("Welcome to Home Page")
    st.write("George R.R. Martin once said:")
    st.write("<i>A reader lives a thousand lives before he dies. The man who never reads lives only one.<i>",unsafe_allow_html=True)
    st.write("<h3>Top 50 Books<h3>", unsafe_allow_html=True)
    names = popular_df['Book-Title'].values
    poster = popular_df['Image-URL-L'].values
    author = popular_df['Book-Author'].values
    avg_rating = popular_df['avg_rating'].values
    num_ratings = popular_df['num_ratings'].values
    start = 0
    for j in range(10):
        col1, col2, col3, col4, col5 = st.columns(5)
        columns = [col1, col2, col3, col4, col5]
        for i in enumerate(start=start, iterable=columns):
            with i[1]:
                st.image(poster[i[0]])
                rating = np.round((avg_rating[i[0]]),2)
                votes  = num_ratings[i[0]]
                expander_state = st.expander(names[i[0]], expanded=False)


                if expander_state:
                    with expander_state:
                        st.markdown(f"<p style='color: #FFFF00;'>Author: {author[i[0]]}</h3>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #FFFF00;'>Average Rating: {rating}</h3>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #FFFF00;'>Votes: {votes}</h3>", unsafe_allow_html=True)
        start = start + 5
        st.write("<br>", unsafe_allow_html=True)
elif user_menu == 'Recommender System':
    st.title("Welcome to Book Recommender System!")
    st.write("Discover personalized book recommendations based on your interests and preferences.")
    unique = books['Book-Title'].unique()
    selected_book_name = st.selectbox("Search Box:", unique)

    if st.button('Recommend'):
        names, posters = recommend(selected_book_name)
        st.header(f"Here are the top 10 Recommendations for {selected_book_name}")

        unique_df = books.drop_duplicates(subset='Book-Title')
        start = 0
        grab_rating = books[['Book-Title', 'Book-Rating']].groupby('Book-Title').mean().reset_index()
        for j in range(2):
            col1, col2, col3, col4, col5 = st.columns(5)
            columns = [col1, col2, col3, col4, col5]
            for i in enumerate(start = start , iterable=columns):
                with i[1]:
                    st.image(posters[i[0]])
                    expander_state = st.expander(names[i[0]], expanded=False)
                    author = unique_df[unique_df['Book-Title'] == names[i[0]]]['Book-Author'].values[0]
                    avg_rating = grab_rating[grab_rating['Book-Title'] == names[i[0]]]['Book-Rating'].values[0]
                    avg_rating = np.round(avg_rating, 2)
                    count = books.groupby('Book-Title').count().reset_index()
                    count = count[count['Book-Title'] == names[i[0]]]['Book-Rating'].values[0]
                    if expander_state:
                        with expander_state:
                            st.markdown(f"<p style='color: #FFFF00;'>Author: {author}</h3>", unsafe_allow_html=True)
                            st.markdown(f"<p style='color:#FFFF00;'>Average Rating:{avg_rating}</p>", unsafe_allow_html=True)
                            st.markdown(f"<p style='color:#FFFF00;'>Votes:{count}</p>",unsafe_allow_html=True)
            st.write("\n"*10)
            start = start + 5
elif user_menu == 'About the Recommender System':

    # Display the header
    st.header("Some Important Things to Know")

    # Display the accompanying text
    st.write(
        "You may have noticed that the average rating and number of ratings for the top 50 books are different when you compare them to the same books recommended by this recommender system. This difference arises because the recommendation system considers only those users who have rated more than 200 books to provide you with the best recommendations. Users who have rated fewer than 200 books are not included in the recommendation process.")

    st.write(
        "This decision was madeto ensure that the recommendations you receive are based on focusing on users with a substantial history of book ratings")

    st.write(
        "Thank you for taking the time to explore this app.I hope you understand and appreciate the reasoning behind this recommendation approach.")





