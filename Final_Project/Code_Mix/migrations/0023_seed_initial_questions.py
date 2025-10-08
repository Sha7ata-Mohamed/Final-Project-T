from django.db import migrations


INITIAL_QUESTIONS = [
    {
        "title": "HTML Basics",
        "question": "What does HTML stand for?",
        "diff_level": "easy",
        "question_category": "html",
        "options": {
            "option_1": "Hyper Trainer Marking Language",
            "option_2": "HyperText Markup Language",
            "option_3": "HyperText Marketing Language",
            "option_4": "Hyper Tool Multi Language",
            "answer": "option_2",
            "explanation": "HTML stands for HyperText Markup Language and is used to structure web pages.",
        },
    },
    {
        "title": "HTML Semantics",
        "question": "Which HTML element best represents self-contained content?",
        "diff_level": "medium",
        "question_category": "html",
        "options": {
            "option_1": "<div>",
            "option_2": "<section>",
            "option_3": "<article>",
            "option_4": "<span>",
            "answer": "option_3",
            "explanation": "<article> is intended for independent, self-contained content.",
        },
    },
    {
        "title": "Python Data Types",
        "question": "Which of the following is an immutable data type in Python?",
        "diff_level": "easy",
        "question_category": "python",
        "options": {
            "option_1": "List",
            "option_2": "Dictionary",
            "option_3": "Set",
            "option_4": "Tuple",
            "answer": "option_4",
            "explanation": "Tuples are immutable sequences in Python.",
        },
    },
    {
        "title": "Python Functions",
        "question": "What keyword is used to define an anonymous function in Python?",
        "diff_level": "medium",
        "question_category": "python",
        "options": {
            "option_1": "def",
            "option_2": "lambda",
            "option_3": "func",
            "option_4": "anonymous",
            "answer": "option_2",
            "explanation": "lambda is used to declare small anonymous functions in Python.",
        },
    },
    {
        "title": "Django Models",
        "question": "Which Django field type is best suited for storing large text?",
        "diff_level": "easy",
        "question_category": "django",
        "options": {
            "option_1": "CharField",
            "option_2": "EmailField",
            "option_3": "TextField",
            "option_4": "SlugField",
            "answer": "option_3",
            "explanation": "TextField is designed for storing large amounts of text in Django models.",
        },
    },
    {
        "title": "Django ORM",
        "question": "Which ORM method returns a new QuerySet containing objects that match the given lookup parameters?",
        "diff_level": "medium",
        "question_category": "django",
        "options": {
            "option_1": "all()",
            "option_2": "create()",
            "option_3": "filter()",
            "option_4": "get_or_create()",
            "answer": "option_3",
            "explanation": "filter() returns a QuerySet matching the provided lookups.",
        },
    },
]


def create_initial_questions(apps, schema_editor):
    Questions = apps.get_model("Code_Mix", "Questions")
    Options = apps.get_model("Code_Mix", "Options")

    for record in INITIAL_QUESTIONS:
        options_data = record["options"]
        question_defaults = {
            "question": record["question"],
            "diff_level": record["diff_level"],
            "question_category": record["question_category"],
        }
        question, created = Questions.objects.get_or_create(
            title=record["title"],
            defaults=question_defaults,
        )
        if not created:
            needs_update = False
            for field, value in question_defaults.items():
                if getattr(question, field) != value:
                    setattr(question, field, value)
                    needs_update = True
            if needs_update:
                question.save(update_fields=list(question_defaults.keys()))

        option_defaults = {
            "option_1": options_data["option_1"],
            "option_2": options_data["option_2"],
            "option_3": options_data["option_3"],
            "option_4": options_data["option_4"],
            "answer": options_data["answer"],
            "title_q": record["title"],
            "explanation": options_data["explanation"],
        }
        Options.objects.update_or_create(
            question=question,
            defaults=option_defaults,
        )


def delete_initial_questions(apps, schema_editor):
    Questions = apps.get_model("Code_Mix", "Questions")
    titles = [record["title"] for record in INITIAL_QUESTIONS]
    Questions.objects.filter(title__in=titles).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("Code_Mix", "0022_rename_user_userdata"),
    ]

    operations = [
        migrations.RunPython(create_initial_questions, delete_initial_questions),
    ]
