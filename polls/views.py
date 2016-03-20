from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from polls.serializers import LanguageSerializer
from polls.serializers import (SituationalVideoSerializer , GrammarVideoSerializer , ExerciseQuestionSerializer,
                               ResourceItemSerializer, ResourceItemNumbersSerializer, ResourceItemPictureSerializer,
                               LevelSerializer, DialectSerializer, GlossarySerializer
                               )
from polls.serializers import SituationalVideo


from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

#from tutorial 3 for language_list()
from django.http import HttpResponse
from django.template import loader

from .models import (
    Language, Topic, LanguageTopic, LanguageSubtopic, ExerciseQuestion, Exercise, ExerciseVocabularyQuestion,
    Dialect, Resource, ResourceItem, ResourceItemPicture, LevelLanguage, Level, Glossary
)
from .forms import (
    LanguageForm, LanguageTopicForm, SituationalVideoForm, LanguageSubtopicForm, ExerciseForm,
    ExerciseQuestionForm, ExerciseVocabularyQuestionForm, LetterResourceForm, NumberResourceForm,
    HolidaysResourceForm, TopicForm, DialectForm, ListeningComprehensionForm, ResourceForm,
    LevelLanguageForm, LevelForm
)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def language_list(request):
    language_list = Language.objects.all()
    context = {'language_list': language_list,}
    return render(request, 'polls/languagelist.html', context)


@csrf_exempt
def grammar_video_list(request, language, level, topic_name, subtopic_name):

    if request.method == 'GET':
        subtopic = LanguageSubtopic.objects.filter(subtopic_name=subtopic_name)
        serializer = GrammarVideoSerializer(subtopic, many=True)
        return JSONResponse(serializer.data)
'''http://127.0.0.1:8000/polls/German/beginner/Bathroom/subtopic-test/grammarVideo/'''

@csrf_exempt
def language_list_show(request):

      if request.method == 'GET':
        language = Language.objects.all()
        serializer = LanguageSerializer(language, many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
def subtopic_list(request, language, level, topic_name):

      if request.method == 'GET':
        language = Language.objects.get(name=language)
        level_name = Level.objects.get(level=level)
        levelLang_name = LevelLanguage.objects.get(level=level_name.id)
        topic_list= Topic.objects.filter(topic_name=topic_name).get(level=levelLang_name.id)
        language_topic= LanguageTopic.objects.filter(language=language.id).get(topic=topic_list.id)
        topic = LanguageSubtopic.objects.filter(language_topic=language_topic.id)
        serializer = GrammarVideoSerializer(topic, many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
def subtopic_list_all(request):

      if request.method == 'GET':
        topic = LanguageSubtopic.objects.all()
        serializer = GrammarVideoSerializer(topic, many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
def situational_video_list(request, language, level, topic_name):

    if request.method == 'GET':
        language = Language.objects.get(name=language)
        level_name = Level.objects.get(level=level)
        levelLang_name = LevelLanguage.objects.get(level=level_name.id)
        topic = Topic.objects.filter(topic_name=topic_name).get(level=levelLang_name.id)
        language_topic = LanguageTopic.objects.filter(language=language.id).get(topic=topic.id)
        video = SituationalVideo.objects.filter(language_topic=language_topic.id)
        serializer = SituationalVideoSerializer(video, many=True)
        return JSONResponse(serializer.data)

def exercise_list(request, language, level, topic_name, subtopic_name):
    if request.method == 'GET':
        language = Language.objects.get(name=language)
        level_name = Level.objects.get(level=level)
        levelLang_name = LevelLanguage.objects.get(level=level_name.id)
        topic = Topic.objects.filter(topic_name=topic_name).get(level=levelLang_name.id)
        language_topic = LanguageTopic.objects.filter(topic=topic.id).get(language=language.id)

        language_subtopic = (LanguageSubtopic.objects.filter(language_topic=language_topic)).get(subtopic_name=subtopic_name)

        exercises = Exercise.objects.filter(language_subtopic=language_subtopic.id)

        to_json = []

        for exercise in exercises:
            exercise_json = {}
            exercise_json['exercise_id'] = exercise.id
            exercise_json['exercise_name'] = exercise.exercise_name

            to_json.append(exercise_json)

        return JsonResponse(to_json, safe=False)


def exercise_question_list(request, language, level, topic_name, subtopic_name, exercise_id):

    if request.method == 'GET':
        exercise = Exercise.objects.get(id=exercise_id)
        exercise_questions = ExerciseQuestion.objects.filter(exercise=exercise.id)

        to_json = {}
        to_json['exercise_name'] = exercise.exercise_name
        to_json['question_type'] = exercise.question_type
        to_json['instructions'] = exercise.instructions
        to_json['instructions_in_language'] = exercise.instructions_in_language
        to_json['exercise_questions'] = []

        for question in exercise_questions:
            exercise_question = {}
            exercise_question['question_text'] = question.question_text
            exercise_question['choice_1'] = question.choice_1
            exercise_question['choice_2'] = question.choice_2
            exercise_question['choice_3'] = question.choice_3
            exercise_question['choice_4'] = question.choice_4
            exercise_question['choice_5'] = question.choice_5
            exercise_question['choice_6'] = question.choice_6
            exercise_question['correct_answer'] = question.correct_answer

            to_json['exercise_questions'].append(exercise_question)


        return JsonResponse(to_json, safe=False)


@csrf_exempt
def dialect_list(request, language):

    if request.method == 'GET':
        language = Language.objects.get(name=language)
        dialect_name = Dialect.objects.filter(language_id=language.id)
        serializer = DialectSerializer(dialect_name , many=True)
        return JSONResponse(serializer.data)

@csrf_exempt
def glossary_api(request, language):

    if request.method == 'GET':
        language = Language.objects.get(name=language)
        words = Glossary.objects.filter(language_id=language.id)
        serializer = GlossarySerializer(words , many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def situational_video_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        situationalVideo = SituationalVideo.objects.get(pk=pk)
    except SituationalVideo.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SituationalVideoSerializer(situationalVideo)
        return JSONResponse(serializer.data)

    elif request.method == 'DELETE':
        situationalVideo.delete()
        return HttpResponse(status=204)

def topic_detail(request, language_name, level, topic_name):
    language = Language.objects.get(name=language_name)
    topic = Topic.objects.get(topic_name=topic_name)

    languagetopic = LanguageTopic.objects.filter(topic=topic.id).get(language=language.id)

    #situational_video = SituationalVideo.objects.get(language_topic=languagetopic.id)
    language_subtopics = LanguageSubtopic.objects.filter(language_topic=languagetopic.id)

    context = {
        'language': language,
        'topic': topic,
        'languagetopic': languagetopic,
        #'situational_video': situational_video,
        'language_subtopics': language_subtopics,
    }

    return render(request, 'polls/languagetopic_detail.html', context)


def language_topic_list(request, language_name, level):
    language = Language.objects.filter(name=language_name)
    level = Level.objects.get(level=level)
    topics = Topic.objects.filter(level=level.id)


    context = {'topic_list': topics,
               'language_name': language_name,
               'level': level,
               'language' : language,
               }

    return render(request, 'polls/topiclist.html', context)

def language_create(request):
    form = LanguageForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url_create())
    else:
        messages.error(request, "Not successfully created")
    if request.method == "POST":
        print(request.POST)

    context = {
        "form": form,
    }
    return render(request, 'polls/language_form.html', context)

def language_update(request, language_id):
    instance = get_object_or_404(Language, id=language_id)
    form = LanguageForm(request.POST or None, instance=instance)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Saved")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")
    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/language_form.html', context)

def language_delete(request, language_id):
    instance = get_object_or_404(Language, name=language_id)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("polls:language_list")

def language_detail(request, language_name):
    language = get_object_or_404(Language, name=language_name)
    levelLangs = LevelLanguage.objects.filter(language=language.id)
    context = {
        'language': language,
        'language_name': language_name,
        'levelLangs': levelLangs
    }
    return render(request, 'polls/language_detail.html', context)

def language_topic_detail(request, language_name, level, topic_name):
    language = Language.objects.get(name=language_name)
    topic = Topic.objects.get(topic_name=topic_name)

    languagetopic = LanguageTopic.objects.filter(topic=topic.id).get(language=language.id)

    try:
        situational_video = SituationalVideo.objects.get(language_topic=languagetopic.id)
    except SituationalVideo.DoesNotExist:
        situational_video = SituationalVideo.objects.none()

    try:
        language_subtopics = LanguageSubtopic.objects.filter(language_topic=languagetopic.id)
    except SituationalVideo.DoesNotExist:
        language_subtopics = LanguageSubtopic.objects.none()

    context = {
        'language': language,
        'topic': topic,
        'languagetopic': languagetopic,
        'situational_video': situational_video,
        'language_subtopics': language_subtopics,
    }

    return render(request, 'polls/languagetopic_detail.html', context)

def language_topic_update(request, language_name, level, topic_name):
    language = Language.objects.get(name=language_name)
    topic = Topic.objects.filter(topic_name=topic_name).get(level=level)

    instance = LanguageTopic.objects.filter(topic=topic.id).get(language=language.id)

    form = LanguageTopicForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")
    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/languagetopic_form.html', context)

def language_topic_create(request, language_name, level):
    language = Language.objects.get(name=language_name)

    form = LanguageTopicForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.language = language
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url_create())
    else:
        messages.error(request, "Not successfully created")

    context = {
        "form": form,
    }
    return render(request, 'polls/languagetopic_form.html', context)

def situational_video_detail(request, language_name, level, topic_name):
    language = Language.objects.get(name=language_name)
    level_name = Level.objects.get(level=level)
    levelLang_name = LevelLanguage.objects.get(level=level_name.id)
    topic = Topic.objects.filter(topic_name=topic_name).get(level=levelLang_name.id)
    languagetopic = LanguageTopic.objects.filter(topic=topic.id).get(language=language.id)

    situational_video = SituationalVideo.objects.filter(language_topic=languagetopic.id)

    context = {
        'language': language,
        'topic': topic,
        'languagetopic': languagetopic,
        'situational_video': situational_video,
    }

    return render(request, 'polls/situational_video_detail.html', context)

def situational_video_update(request, language_name, level, topic_name):
    language = Language.objects.get(name=language_name)
    level_name = Level.objects.get(level=level)
    levelLang_name = LevelLanguage.objects.filter(level=level_name.id).get(language=language.id)
    topic = Topic.objects.filter(topic_name=topic_name).get(level=levelLang_name.id)
    languagetopic = LanguageTopic.objects.filter(topic=topic.id).get(language=language.id)

    instance = SituationalVideo.objects.get(language_topic=languagetopic.id)

    form = SituationalVideoForm(request.POST or None, instance=instance)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Saved")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")
    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/situational_video_form.html', context)

def situational_video_create(request, language_name, level, topic_name):
    form = SituationalVideoForm(request.POST or None, instance=instance)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Saved")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")
    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/situational_video_form.html', context)

def subtopic_detail(request, language_name, level, topic_name, subtopic_name):
    language = Language.objects.get(name=language_name)
    level_name = Level.objects.get(level=level)
    langLevel = LevelLanguage.objects.get(level=level_name.id)
    topic = Topic.objects.filter(topic_name=topic_name).get(level=langLevel.id)
    languagetopic = LanguageTopic.objects.filter(topic=topic.id).get(language=language.id)

    language_subtopic = LanguageSubtopic.objects.filter(language_topic=languagetopic.id).get(subtopic_name=subtopic_name)
    exercises = Exercise.objects.filter(language_subtopic=language_subtopic.id)

    questions = []
    for exercise in exercises:
        questions.append(ExerciseQuestion.objects.filter(exercise=exercise.id))

    vocab_questions = []
    if len(exercises)>1:
        vocab_questions = ExerciseVocabularyQuestion.objects.filter(exercise=exercises[0].id)

    context = {
        'language': language,
        'topic': topic,
        'languagetopic': languagetopic,
        'language_subtopic': language_subtopic,
        'exercises': exercises,
        'questions': questions,
        'vocab_questions': vocab_questions,

    }

    return render(request, 'polls/language_subtopic_detail.html', context)

def subtopic_create(request, language_name, level, topic_name):

    language = Language.objects.get(name=language_name)
    topic = Topic.objects.filter(topic_name=topic_name).get(level=level)
    language_topic = LanguageTopic.objects.filter(topic=topic.id).get(language=language.id)

    form = LanguageSubtopicForm(request.POST or None)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.language_topic = language_topic
            instance.save()
            messages.success(request, "Successfully created")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully created")
    if request.method == "POST":
        print(request.POST)

    context = {
        "form": form,
    }
    return render(request, 'polls/language_subtopic_form.html', context)

def subtopic_update(request, language_name, level, topic_name, subtopic_name):
    language = Language.objects.get(name=language_name)
    level_name = Level.objects.get(level=level)
    levelLang_name = LevelLanguage.objects.get(level=level_name.id)
    topic = Topic.objects.filter(topic_name=topic_name).get(level=levelLang_name.id)
    languagetopic = LanguageTopic.objects.filter(topic=topic.id).get(language=language.id)


    instance = LanguageSubtopic.objects.filter(language_topic=languagetopic.id).get(subtopic_name=subtopic_name)

    form = LanguageSubtopicForm(request.POST or None, instance=instance)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Saved")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")

    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/language_subtopic_form.html', context)

def exercise_detail(request, language_name, level, topic_name, subtopic_name, exercise_id):
    language = Language.objects.get(name=language_name)
    topic = Topic.objects.filter(topic_name=topic_name).get(level=level)
    languagetopic = LanguageTopic.objects.filter(topic=topic.id).get(language=language.id)
    language_subtopic = LanguageSubtopic.objects.filter(language_topic=languagetopic.id).get(subtopic_name=subtopic_name)


    context = {
        'language': language,
        'topic': topic,
        'languagetopic': languagetopic,
        'language_subtopic': language_subtopic,


    }

    return render(request, 'polls/exercise_detail.html', context)

def exercise_create(request, language_name, level, topic_name, subtopic_name):
    language = Language.objects.get(name=language_name)
    level_name = Level.objects.get(level=level)
    levelLang_name = LevelLanguage.objects.get(level=level_name.id)
    topic = Topic.objects.filter(topic_name=topic_name).get(level=levelLang_name.id)
    languagetopic = LanguageTopic.objects.filter(topic=topic.id).get(language=language.id)
    language_subtopic = LanguageSubtopic.objects.filter(language_topic=languagetopic.id).get(subtopic_name=subtopic_name)

    form = ExerciseForm(request.POST or None)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.language_subtopic = language_subtopic
            instance.save()
            messages.success(request, "Successfully created")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully created")
    if request.method == "POST":
        print(request.POST)

    context = {
        "form": form,
    }
    return render(request, 'polls/exercise_form.html', context)

def exercise_update(request, language_name, level, topic_name, subtopic_name, exercise_id):
    instance = Exercise.objects.get(id=exercise_id)


    form = ExerciseForm(request.POST or None, instance=instance)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Saved")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")

    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/exercise_form.html', context)


def exercise_question_detail(request, language_name, level, topic_name, subtopic_name, exercise_id, question_id):
    language = Language.objects.get(name=language_name)
    topic = Topic.objects.filter(topic_name=topic_name).get(level=level)
    languagetopic = LanguageTopic.objects.filter(topic=topic.id).get(language=language.id)
    language_subtopic = LanguageSubtopic.objects.filter(language_topic=languagetopic.id).get(subtopic_name=subtopic_name)

    exercise = Exercise.objects.get(id=exercise_id)
    questions = ExerciseQuestion.objects.filter(id=question_id)

    context = {
        'language': language,
        'topic': topic,
        'languagetopic': languagetopic,
        'language_subtopic': language_subtopic,
        'exercise': exercise,
        'questions': questions,
    }

    return render(request, 'polls/exercise_question_detail.html', context)

def exercise_question_update(request, language_name, level, topic_name, subtopic_name, exercise_id, question_id):
    instance = ExerciseQuestion.objects.get(id=question_id)

    form = ExerciseQuestionForm(request.POST or None, instance=instance)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Saved")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")

    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/exercise_question_form.html', context)

def exercise_question_create(request, language_name, level, topic_name, subtopic_name, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)

    form = ExerciseQuestionForm(request.POST or None)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.exercise = exercise
            instance.save()
            messages.success(request, "Successfully created")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully created")
    if request.method == "POST":
        print(request.POST)

    context = {
        "form": form,
    }
    return render(request, 'polls/exercise_question_form.html', context)

def exercise_vocab_question_detail(request, language_name, level, topic_name, subtopic_name, exercise):
    language = Language.objects.get(name=language_name)
    topic = Topic.objects.filter(topic_name=topic_name).get(level=level)
    languagetopic = LanguageTopic.objects.filter(topic=topic.id).get(language=language.id)
    language_subtopic = LanguageSubtopic.objects.filter(language_topic=languagetopic.id).get(subtopic_name=subtopic_name)

    exercise = Exercise.objects.get(language_subtopic=language_subtopic.id)
    vocab_questions = ExerciseVocabularyQuestion.objects.filter(exercise=exercise.id)

    context = {
        'language': language,
        'topic': topic,
        'languagetopic': languagetopic,
        'language_subtopic': language_subtopic,
        'exercise': exercise,
        'vocab_questions': vocab_questions,
    }

    return render(request, 'polls/exercise_vocab_question_detail.html', context)

def exercise_vocab_question_update(request, language_name, level, topic_name, subtopic_name, vocab_question_id):

    instance = ExerciseVocabularyQuestion.objects.get(id=vocab_question_id)

    form = ExerciseVocabularyQuestionForm(request.POST or None, instance=instance)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Saved")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")

    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/exercise_vocab_question_form.html', context)

def choose_dialect(request, language_name):
    language = Language.objects.get(name=language_name)
    dialects = Dialect.objects.filter(language_id=language)

    context = {
        'language_name': language_name,
        'dialects': dialects,
    }

    return render(request, 'polls/choose_dialect.html', context)

def language_resources(request, language_name, dialect):

    context = {
        'language_name': language_name,
        'dialect': dialect,
    }

    return render(request, 'polls/language_resources.html', context)

def language_resources_alphabet(request, language_name, dialect):
    resource_name = "Alphabet"
    dialect = Dialect.objects.get(name=dialect)

    try:
        resource = Resource.objects.filter(dialect_id=dialect.id).get(name=resource_name)
    except Resource.DoesNotExist:
        resource = Resource(dialect_id= dialect, name=resource_name, name_in_language=resource_name, instructions="inst", instructions_in_language="inst")
        resource.save()

    items = ResourceItem.objects.filter(resource_id=resource.id)

    context = {
        'language_name': language_name,
        'dialect': dialect,
        'items': items,
        'resource_name': resource_name,
    }

    return render(request, 'polls/resource_alphabet.html', context)

def letter_resource_update(request, language_name, dialect, resource_id):
    instance = ResourceItem.objects.get(id=resource_id)

    form = LetterResourceForm(request.POST or None, instance=instance)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Saved")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")

    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/language_resource_form.html', context)

def letter_resource_create(request, language_name, dialect):
    dialect = Dialect.objects.get(name=dialect)
    resource = Resource.objects.filter(dialect_id=dialect.id).get(name="Alphabet")

    form = LetterResourceForm(request.POST or None)

    if form.is_valid():
            instance = form.save(commit=False)
            instance.resource_id = resource
            instance.save()
            messages.success(request, "Successfully created")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully created")
    if request.method == "POST":
        print(request.POST)

    context = {
        "form": form,
    }
    return render(request, 'polls/language_resource_form.html', context)

def language_resources_numbers(request, language_name, dialect):
    resource_name = "Numbers"
    dialect = Dialect.objects.get(name=dialect)

    try:
        resource = Resource.objects.filter(dialect_id=dialect.id).get(name=resource_name)
    except Resource.DoesNotExist:
        resource = Resource(dialect_id= dialect, name=resource_name, name_in_language=resource_name, instructions="inst", instructions_in_language="inst")
        resource.save()

    items = ResourceItem.objects.filter(resource_id=resource.id)

    context = {
        'language_name': language_name,
        'dialect': dialect,
        'items': items,
        'resource_name': resource_name,
    }

    return render(request, 'polls/resource_numbers.html', context)

def number_resource_update(request, language_name, dialect, resource_id):
    instance = ResourceItem.objects.get(id=resource_id)

    form = NumberResourceForm(request.POST or None, instance=instance)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Saved")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")

    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/resource_numbers_form.html', context)

def number_resource_create(request, language_name, dialect):
    resource_name = "Numbers"
    dialect = Dialect.objects.get(name=dialect)
    resource = Resource.objects.filter(dialect_id=dialect.id).get(name=resource_name)

    form = NumberResourceForm(request.POST or None)

    if form.is_valid():
            instance = form.save(commit=False)
            instance.resource_id = resource
            instance.save()
            messages.success(request, "Successfully created")
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully created")
    if request.method == "POST":
        print(request.POST)

    context = {
        "form": form,
    }
    return render(request, 'polls/resource_numbers_form.html', context)

def resources_days(request, language_name, dialect):
    resource_name = "Days"
    dialect = Dialect.objects.get(name=dialect)

    try:
        resource = Resource.objects.filter(dialect_id=dialect.id).get(name=resource_name)
    except Resource.DoesNotExist:
        resource = Resource(dialect_id= dialect, name=resource_name, name_in_language=resource_name, instructions="inst", instructions_in_language="inst")
        resource.save()

    items = ResourceItem.objects.filter(resource_id=resource.id)

    context = {
        'language_name': language_name,
        'dialect': dialect,
        'items': items,
        'resource_name': resource_name,
    }

    return render(request, 'polls/resource_days.html', context)

def days_resource_update(request, language_name, dialect, resource_id):
    instance = ResourceItem.objects.get(id=resource_id)

    form = NumberResourceForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")

    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/resource_days_form.html', context)

def days_resource_create(request, language_name, dialect):
    resource_name = "Days"
    dialect = Dialect.objects.get(name=dialect)
    resource = Resource.objects.filter(dialect_id=dialect.id).get(name=resource_name)

    form = NumberResourceForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.resource_id = resource
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully created")

    context = {
        "form": form,
    }
    return render(request, 'polls/resource_days_form.html', context)

def resources_holidays(request, language_name, dialect):
    resource_name = "Holidays"
    dialect = Dialect.objects.get(name=dialect)

    try:
        resource = Resource.objects.filter(dialect_id=dialect.id).get(name=resource_name)
    except Resource.DoesNotExist:
        resource = Resource(dialect_id= dialect, name=resource_name, name_in_language=resource_name, instructions="inst", instructions_in_language="inst")
        resource.save()


    items = ResourceItemPicture.objects.filter(resource_id=resource.id)

    context = {
        'language_name': language_name,
        'dialect': dialect,
        'items': items,
        'resource_name': resource_name,
    }

    return render(request, 'polls/resource_holidays.html', context)

def holidays_resource_update(request, language_name, dialect, resource_id):
    instance = ResourceItemPicture.objects.get(id=resource_id)

    form = HolidaysResourceForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")

    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/resource_holidays_form.html', context)

def holidays_resource_create(request, language_name, dialect):
    resource_name = "Holidays"
    dialect = Dialect.objects.get(name=dialect)
    resource = Resource.objects.filter(dialect_id=dialect.id).get(name=resource_name)

    form = HolidaysResourceForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.resource_id = resource
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully created")

    context = {
        "form": form,
    }
    return render(request, 'polls/resource_holidays_form.html', context)

def resources_months(request, language_name, dialect):
    resource_name = "Months"
    dialect = Dialect.objects.get(name=dialect)

    try:
        resource = Resource.objects.filter(dialect_id=dialect.id).get(name=resource_name)
    except Resource.DoesNotExist:
        resource = Resource(dialect_id= dialect, name=resource_name, name_in_language=resource_name, instructions="inst", instructions_in_language="inst")
        resource.save()

    items = ResourceItem.objects.filter(resource_id=resource.id)

    context = {
        'language_name': language_name,
        'dialect': dialect,
        'items': items,
        'resource_name': resource_name,
        'resource': resource,
    }

    return render(request, 'polls/resource_months.html', context)

def resources_edit(request, language_name, dialect, resource_name):
    dialect = Dialect.objects.get(name=dialect)
    instance = Resource.objects.filter(dialect_id=dialect.id).get(name=resource_name)

    form = ResourceForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")

    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/resource_form.html', context)

def months_resource_update(request, language_name, dialect, season_or_month_name):
    #TODO can only take in one dialect name, dialect must be unique, also season_or_month_name
    dialect_object = Dialect.objects.get(name=dialect)
    resource = Resource.objects.filter(dialect_id=dialect_object.id).get(name="Months")
    try:
        instance = ResourceItem.objects.filter(resource_id=resource.id).get(word=season_or_month_name)
    except ResourceItem.DoesNotExist:
        instance = ResourceItem(resource_id=resource, word=season_or_month_name)
        instance.save()

    form = NumberResourceForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")

    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/resource_months_form.html', context)

def months_resource_create(request, language_name, dialect):
    resource_name = "Months"
    dialect = Dialect.objects.get(name=dialect)
    resource = Resource.objects.filter(dialect_id=dialect.id).get(name=resource_name)

    form = NumberResourceForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.resource_id = resource
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully created")

    context = {
        "form": form,
    }
    return render(request, 'polls/resource_months_form.html', context)


def resources_time(request, language_name, dialect):
    resource_name = "Time"
    dialect = Dialect.objects.get(name=dialect)

    try:
        resource = Resource.objects.filter(dialect_id=dialect.id).get(name=resource_name)
    except Resource.DoesNotExist:
        resource = Resource(dialect_id= dialect, name=resource_name, name_in_language=resource_name, instructions="inst", instructions_in_language="inst")
        resource.save()

    items = ResourceItemPicture.objects.filter(resource_id=resource.id)

    context = {
        'language_name': language_name,
        'dialect': dialect,
        'items': items,
        'resource_name': resource_name,
    }

    return render(request, 'polls/resource_time.html', context)

def time_resource_update(request, language_name, dialect, resource_id):
    instance = ResourceItemPicture.objects.get(id=resource_id)

    form = HolidaysResourceForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")

    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/resource_time_form.html', context)

def time_resource_create(request, language_name, dialect):
    resource_name = "Time"
    dialect = Dialect.objects.get(name=dialect)
    resource = Resource.objects.filter(dialect_id=dialect.id).get(name=resource_name)

    form = HolidaysResourceForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.resource_id = resource
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully created")

    context = {
        "form": form,
    }
    return render(request, 'polls/resource_time_form.html', context)

def dashboard(request):
    language_list = Language.objects.all()
    levels = Level.objects.all()
    context = {
        'language_list': language_list,
        'levels': levels,
    }
    return render(request, 'polls/dashboard.html', context)

def level_detail(request, level):
    level = Level.objects.get(level=level)
    topics = Topic.objects.filter(level=level)
    context = {
        'level': level,
        'topics': topics,
    }
    return render(request, 'polls/level_detail.html', context)

def topic_update(request, level, topic_id):
    instance = Topic.objects.get(id=topic_id)

    form = TopicForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")

    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/topic_form.html', context)

def topic_create(request, level):
    form = TopicForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.level = level
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully created")

    context = {
        "form": form,
    }
    return render(request, 'polls/topic_form.html', context)

def dialect_create(request, language_name):
    language = Language.objects.get(name=language_name)

    form = DialectForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.language_id = language
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully created")

    context = {
        "form": form,
    }
    return render(request, 'polls/dialect_form.html', context)

def dialect_update(request, language_name, dialect_id):
    instance = Dialect.objects.get(id=dialect_id)

    form = DialectForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")

    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/dialect_form.html', context)


def listening_comprehension_update(request, language_name, level, topic_name, sv_id):
    instance = SituationalVideo.objects.get(id=sv_id)

    form = ListeningComprehensionForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully saved")

    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, 'polls/listening_comprehension_form.html', context)


def situational_video_list_temp(request, language_name, level, topic_name):
    to_json = {
        "language_topic": "2",
        "situation_description": "In the park",
        "situation_description_in_language": "En el parque",
        "video_with_transcript": "media/U01-01.mp4",
        "video_without_transcript": "media/U01-02.mp4",
    }

    return JsonResponse(to_json)

def grammar_video_list_temp(request, language_name, level, topic_name, subtopic_name):
    to_json = {
        "language_topic": "2",
        "subtopic_name": "Pronouns",
        "subtopic_name_in_language": "Pronombres",
        "grammar_video_file": "media/U01-01-Gra-Pronombres.mp4",
    }

    return JsonResponse(to_json)

def exercise_question_list_temp(request, language_name, level, topic_name, subtopic_name):
    if subtopic_name=="Vocabulary":
        to_json = [
            {
                "exercise": "2",
                "question_text": "tren",
                "choice_1": "media/vocabulary/U01-02-train.png",
                "choice_2": "media/vocabulary/U01-03-airplane.png",
                "choice_3": "media/vocabulary/U01-05-ship.png",
                "choice_4": "media/vocabulary/U01-07-bus.png",
                "choice_5": "media/vocabulary/U01-10-bike.png",
                "choice_6": "media/vocabulary/U01-09-car.png",
                "correct_answer": "1",
            },
            {
                "exercise": "2",
                "question_text": "avión",
                "choice_1": "media/vocabulary/U01-02-train.png",
                "choice_2": "media/vocabulary/U01-03-airplane.png",
                "choice_3": "media/vocabulary/U01-05-ship.png",
                "choice_4": "media/vocabulary/U01-07-bus.png",
                "choice_5": "media/vocabulary/U01-10-bike.png",
                "choice_6": "media/vocabulary/U01-09-car.png",
                "correct_answer": "2",
            },
            {
                "exercise": "2",
                "question_text": "coche",
                "choice_1": "media/vocabulary/U01-02-train.png",
                "choice_2": "media/vocabulary/U01-03-airplane.png",
                "choice_3": "media/vocabulary/U01-05-ship.png",
                "choice_4": "media/vocabulary/U01-07-bus.png",
                "choice_5": "media/vocabulary/U01-10-bike.png",
                "choice_6": "media/vocabulary/U01-09-car.png",
                "correct_answer": "6",
            },
            {
                "exercise": "2",
                "question_text": "autobús",
                "choice_1": "media/vocabulary/U01-02-train.png",
                "choice_2": "media/vocabulary/U01-03-airplane.png",
                "choice_3": "media/vocabulary/U01-05-ship.png",
                "choice_4": "media/vocabulary/U01-07-bus.png",
                "choice_5": "media/vocabulary/U01-10-bike.png",
                "choice_6": "media/vocabulary/U01-09-car.png",
                "correct_answer": "4",
            },
        ]
    else:
        to_json = [
            {
                "exercise": "1",
                "question_text": "___ te llamas",
                "choice_1": "vosotros",
                "choice_2": "él/ella/usted",
                "choice_3": "yo",
                "choice_4": "tú",
                "choice_5": "nosotros",
                "choice_6": "ellos/ellas/ustedes",
                "correct_answer": "2",
            },
            {
                "exercise": "1",
                "question_text": "___ se llaman",
                "choice_1": "vosotros",
                "choice_2": "él/ella/usted",
                "choice_3": "yo",
                "choice_4": "tú",
                "choice_5": "nosotros",
                "choice_6": "ellos/ellas/ustedes",
                "correct_answer": "6",
            },
            {
                "exercise": "1",
                "question_text": "___ os llamáis",
                "choice_1": "vosotros",
                "choice_2": "él/ella/usted",
                "choice_3": "yo",
                "choice_4": "tú",
                "choice_5": "nosotros",
                "choice_6": "ellos/ellas/ustedes",
                "correct_answer": "1",
            },
            {
                "exercise": "1",
                "question_text": "___ me llamo",
                "choice_1": "vosotros",
                "choice_2": "él/ella/usted",
                "choice_3": "yo",
                "choice_4": "tú",
                "choice_5": "nosotros",
                "choice_6": "ellos/ellas/ustedes",
                "correct_answer": "3",
            },
        ]


    return JsonResponse(to_json, safe=False)

def subtopic_list_temp(request, language_name, level, topic_name):
    to_json = [
        {
        "language_topic": "2",
        "subtopic_name": "Pronouns",
        "subtopic_name_in_language": "Pronombres",
        },
        {
        "language_topic": "2",
        "subtopic_name": "Llamarse",
        "subtopic_name_in_language": "Llamarse",
        },
        {
        "language_topic": "2",
        "subtopic_name": "Ser and Estar",
        "subtopic_name_in_language": "Ser y Estar",
        },
        {
        "language_topic": "2",
        "subtopic_name": "Vocabulary",
        "subtopic_name_in_language": "Vocabulario",
        },
    ]

    return JsonResponse(to_json, safe=False)

def listening_comprehension_temp(request, language_name, level, topic_name):
    to_json = {
        "exercise": "1",
        "audio_url": "media/listening_comprehension/U01-E05.mp3",
        "choice_1": "Marta llega a Madrid en tren",
        "choice_2": "Peter es amigo de Julia",
        "choice_3": "Julia presenta a Julia y Peter",
        "choice_4": "Julia pregunta dónde está su amigo",
        "choice_5": "Todos están en la estación de tren",
        "choice_6": "Peter esta en España",
        "correct_answers": "2,3,4,5,6",
    }

    return JsonResponse(to_json)

def resource_api(request, language_name, dialect, resource_name):
    if request.method == 'GET':
        dialect = Dialect.objects.get(name=dialect)
        resource = Resource.objects.filter(dialect_id=dialect.id).get(name=resource_name)
        resource_items = ResourceItem.objects.filter(resource_id=resource.id)

        if resource_name=="Alphabet" or resource_name=="Months":
            serializer = ResourceItemSerializer(resource_items, many=True)
        elif resource_name=="Numbers" or resource_name=="Days":
            serializer = ResourceItemNumbersSerializer(resource_items, many=True)
        elif resource_name=="Holidays" or resource_name=="Time":
            serializer = ResourceItemPictureSerializer(resource_items, many=True)

    return JSONResponse(serializer.data)

def level_api(request, language_name):
    if request.method == 'GET':
        language = Language.objects.get(name=language_name)
        levellang = LevelLanguage.objects.filter(language=language.id)
        levels = []
        for level in levellang:
            levels.append(Level.objects.get(level=level.level))

        serializer = LevelSerializer(levels, many=True)

    return JSONResponse(serializer.data)

def level_language_create(request, language_name):
    language = Language.objects.get(name=language_name)

    form = LevelLanguageForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.language = language
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        #messages.error(request, "Not successfully created")
        pass

    context = {
        "form": form,
    }
    return render(request, 'polls/resource_time_form.html', context)

def level_create(request):
    form = LevelForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        #messages.error(request, "Not successfully created")
        pass

    context = {
        "form": form,
    }
    return render(request, 'polls/resource_time_form.html', context)