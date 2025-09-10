import requests ,html ,threading ,time ,os ,random ,sys 

CATEGORY_URL = "https://opentdb.com/api_category.php"
QUESTION_URL = "https://opentdb.com/api.php"
TIME_LIMIT = 15 

#api_func_defs

def retrieve_categories():
    try:
        r= requests.get(CATEGORY_URL)
        return r.json().get("trivia_categories", [])
    except requests.exceptions.RequestException:                         
        print("Some error occured")
        return []

def retrieve_questions(amount):
    global difficulty, category, qtype
    details= {"amount": amount}
    if difficulty:
        details["difficulty"] = difficulty
    if qtype:
        details["type"] = qtype
    if category:
        details["category"] = category

    try:
        response = requests.get(QUESTION_URL, params=details)
        return response.json().get("results", [])
    except:
        print("Error occurred")
        return []
    
# func_defs for selection

def sel_category(cat):
    print("\nSelect category:")
    i = 1
    for j in cat:
        print(str(i)+". "+j["name"])      
        i = i + 1

    choice = input("Enter category number (press enter for selecting random category): ")
    if choice == "":
        return None

    try:
        return cat[int(choice)-1]["id"]
    except:
        print("Using Random Category!")
        return None

def sel_question_type():
    qtype = ["multiple", "boolean"]
    print("\nSelect question type:")
    i = 1
    for q in qtype:
        print(str(i)+". "+q)
        i = i + 1

    choice = input("Enter question type number (press enter for selecting random): ")
    if choice == "":
        return None
    try:
        return qtype[int(choice) - 1]
    except:
        print("Using random question type!")
        return None


def sel_difficulty():
    difficulty = ["easy", "medium", "hard"]
    print("\nSelect difficulty:")
    i = 1
    for d in difficulty:
        print(str(i)+". "+d)
        i = i + 1

    choice = input("Enter a difficulty number (or press enter for random): ")
    if choice == "":
        return None
    try:
        return difficulty[int(choice)-1]
    except:
        print("Using Random difficulty!")
        return None

#quiz 

def question_related(question_data):
    question = html.unescape(question_data["question"])                   # Newly learnt what unescape does
    correct_ans= html.unescape(question_data["correct_answer"])
    options = [html.unescape(a) for a in question_data["incorrect_answers"]]
    options.append(correct_ans)
    random.shuffle(options)     #this randomizes order of options
    print("\nQuestion: "+question)
    i = 1
    for opt in options:
        print(str(i)+". "+opt)
        i += 1

    print("You should answer in " + str(TIME_LIMIT) + " seconds.")

    answer = [None]
    timed_out = [0]

    def get_input():
        ans = input("Enter your answer (opt number): ")
        if timed_out[0] == 0:
            answer[0] = ans

    def countdown():
        time.sleep(TIME_LIMIT)
        if answer[0] is None:
            timed_out[0] = 1
            print("\nTime's finished")

    input_thread = threading.Thread(target=get_input)                  #threading is used to work mutliple things at once
    timer_thread = threading.Thread(target=countdown)

    input_thread.start()
    timer_thread.start()

    input_thread.join(TIME_LIMIT)

    if timed_out[0] == 1 and answer[0] is None:
        return False 

    try:
        ans = int(answer[0])
        chosen = options[ans - 1] 
    except:
        print("Invalid answer :|")
        return False

    if chosen == correct_ans:
        print("Its Correct :)")
        return True
    else:
        print("Its Incorrect :( Correct answer: " + correct_ans)
        return False


def select_quiz_options(categories):
    global category, difficulty, qtype
    category = sel_category(categories)
    difficulty = sel_difficulty()
    qtype = sel_question_type()


#main 

def main():
    print("TimeTickQuiz WELCOMES YOU")
    print("Wish you all the best")
    categories = retrieve_categories()
    if not categories:                                                    # mentioning error cases
        print("Categories unavailable")          
        return

    select_quiz_options(categories)
    amount = int (input ("\nEnter no: of problems required:"))
    questions = retrieve_questions(amount)
    if not questions:
        print("Questions not retrieved")
        return

    score = 0
    for q in questions:
        if question_related(q):
            score += 1

    print("\nYour final score: " + str(score) + "/" + str(len(questions)))
    sys.exit(0)


if __name__ == "__main__":
    main()