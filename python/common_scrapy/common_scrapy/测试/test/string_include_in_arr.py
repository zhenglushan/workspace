filter_word = [
    ["清明", "清明节"],
    ["图片", "素材", "模板", "海报", "PPT"]
]
text = "我在收集有关于清明节的相关素材和模板"
matches = [(word1,word2)
           for word1 in filter_word[0] if word1 in text
           for word2 in filter_word[1] if word2 in text
        ]
print(matches)
print(len(matches))