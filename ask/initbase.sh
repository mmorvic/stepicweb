#!/bin/bash                                                                                                   
for i in `seq 1 100`;
do
    mysql -uroot -e "INSERT INTO ask.question_post (title, text,  author_id) VALUES ('title$i', 'query_post_text$i',  '1');"
done 