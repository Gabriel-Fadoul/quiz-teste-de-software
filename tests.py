import pytest
from model import Question

@pytest.fixture
def question_test_template():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', False)
    question.add_choice('c', True)
    question.add_choice('d', False)
    question.add_choice('e', False)
    return question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct


def test_create_question_with_invalid_points():
    with pytest.raises(Exception, match="Points must be between 1 and 100"):
        Question(title="Q", points=0)

def test_create_choice_with_empty_text():
    question = Question(title='q1')
    
    with pytest.raises(Exception, match="Text cannot be empty"):
        question.add_choice('', False)
        
def test_create_choice_with_text_too_long():
    question = Question(title='q1')
    
    with pytest.raises(Exception, match="Text cannot be longer than 100 characters"):
        question.add_choice('ABC'*35, False)
        
def test_remove_choice_by_id():
    q = Question("Question test ")
    choice = q.add_choice("Option A")
    q.remove_choice_by_id(choice.id)
    assert len(q.choices) == 0
    
def test_remove_choice_by_id_invalid_id():
    q = Question("Question test")
    with pytest.raises(Exception, match="Invalid choice id"):
        q.remove_choice_by_id(999)
    
def test_remove_all_choices_valid():
    q = Question("Question test")
    q.add_choice("A")
    q.add_choice("B")
    q.remove_all_choices()
    assert q.choices == []

def test_select_choices_valid():
    q = Question("Question test")
    a = q.add_choice("A", is_correct=True)
    b = q.add_choice("B", is_correct=False)
    selected = q.select_choices([a.id])
    assert selected == [a.id]
    
def test_select_choices_multiple_choices_exception():
    q = Question("Question test", max_selections=1)
    a = q.add_choice("A")
    b = q.add_choice("B")
    with pytest.raises(Exception, match="Cannot select more than 1 choices"):
        q.select_choices([a.id, b.id])
        
def test_select_choices_invalid_choices():
    q = Question("Q?")
    a = q.add_choice("A", is_correct=False)
    assert q.select_choices([a.id]) == []

def test_set_correct_choices_valid():
    q = Question("Question test")
    a = q.add_choice("A")
    q.set_correct_choices([a.id])
    assert a.is_correct is True
    
def test_set_correct_choices_invalid_id(question_test_template):
    with pytest.raises(Exception, match="Invalid choice id"):
        question_test_template.set_correct_choices([999])
        
def test_add_choice_increment_id(question_test_template):
    c1 = question_test_template.add_choice("A")
    c2 = question_test_template.add_choice("B")
    assert c1.id == 6
    assert c2.id == 7