
def mathingWords(sentence1, sentence2):
    words1 = sentence1.strip().split(" ")
    words2 = sentence2.strip().split(" ")
    score = 0
    for word1 in words1:
        for word2 in words2:
            # print(f"Matching {word1} with {word2}")
            if word1.lower() == word2.lower():
                score += 1
    return score


sentences = ["python is a good", "this is snake",
             "harry is a good boy", "Subscribe to code with harry"]

query = input("Please enter the query string\n")
# scores = [mathingWords(query, sentence) for sentence in sentences]
scores = []
for sentence in sentences:
    scores.append(mathingWords(query, sentence))

# sortedSentScore = [sentScore for sentScore in sorted(zip(scores, sentences), reverse=True) if sentScore[0] != 0]

list1= zip(scores, sentences)

sortedSentScore = []
for sentScore in sorted(list1, reverse=True):
    if sentScore[0] != 0:
        sortedSentScore.append(sentScore)

print(f"{len(sortedSentScore)} results found!")
for score, item in sortedSentScore:
    print(f" \"{item}\": with a score of {score}")
