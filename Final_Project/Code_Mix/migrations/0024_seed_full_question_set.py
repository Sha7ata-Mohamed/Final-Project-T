from django.db import migrations


def get_question_records():
    questions = []

    def add_group(category, difficulty, items):
        for idx, item in enumerate(items, start=1):
            title = f"{category.upper()} {difficulty.title()} Q{idx}: {item['title']}"
            questions.append(
                {
                    "title": title,
                    "question": item["question"],
                    "diff_level": difficulty,
                    "question_category": category,
                    "options": {
                        "option_1": item["options"][0],
                        "option_2": item["options"][1],
                        "option_3": item["options"][2],
                        "option_4": item["options"][3],
                        "answer": item["answer"],
                        "explanation": item["explanation"],
                    },
                }
            )

    add_group(
        "html",
        "easy",
        [
            {
                "title": "Purpose of <head>",
                "question": "Which statement best describes the purpose of the HTML <head> element?",
                "options": [
                    "It renders visible page content.",
                    "It holds metadata like title and links to styles.",
                    "It displays the page header banner.",
                    "It wraps the main article.",
                ],
                "answer": "option_2",
                "explanation": "<head> contains metadata (title, meta tags, linked styles/scripts) used by browsers.",
            },
            {
                "title": "Line Break Element",
                "question": "Which HTML tag inserts a line break?",
                "options": ["<break>", "<br>", "<lb>", "<p>"],
                "answer": "option_2",
                "explanation": "<br> creates a single line break within text content.",
            },
            {
                "title": "Image Alt Text",
                "question": "Why should every <img> tag include the alt attribute?",
                "options": [
                    "It styles the image border.",
                    "It loads higher quality images.",
                    "It provides alternative text for accessibility and fallbacks.",
                    "It caches the image for offline use.",
                ],
                "answer": "option_3",
                "explanation": "The alt attribute conveys content to screen readers and when the image cannot load.",
            },
            {
                "title": "Hyperlink Creation",
                "question": "Which attribute is required to create a hyperlink with the <a> tag?",
                "options": ["src", "href", "target", "rel"],
                "answer": "option_2",
                "explanation": "The href attribute specifies the destination URL for a hyperlink.",
            },
            {
                "title": "Semantic Paragraph",
                "question": "Which HTML element is used for a paragraph of text?",
                "options": ["<span>", "<section>", "<p>", "<article>"],
                "answer": "option_3",
                "explanation": "<p> represents a paragraph and provides semantic meaning for blocks of text.",
            },
        ],
    )

    add_group(
        "html",
        "medium",
        [
            {
                "title": "Semantic Navigation",
                "question": "Which element best wraps a set of primary navigation links?",
                "options": ["<nav>", "<aside>", "<main>", "<menuitem>"],
                "answer": "option_1",
                "explanation": "<nav> communicates a block of navigation links to both browsers and assistive tech.",
            },
            {
                "title": "Responsive Images",
                "question": "Which attribute ensures an <img> scales with its container in CSS layouts?",
                "options": ["height='auto'", "width='100px'", "style='max-width:100%; height:auto;'", "class='responsive-cover'"],
                "answer": "option_3",
                "explanation": "Using max-width:100% and height:auto allows the image to shrink or grow with its container.",
            },
            {
                "title": "Tables and Accessibility",
                "question": "What attribute pairs table headers with data cells for accessibility?",
                "options": ["scope", "align", "colspan", "cellpadding"],
                "answer": "option_1",
                "explanation": "scope on <th> elements helps screen readers associate headers with data cells.",
            },
            {
                "title": "Forms and Labels",
                "question": "How do you explicitly link a <label> to a form control?",
                "options": [
                    "Place the label after the input.",
                    "Set label's for attribute to the input's id.",
                    "Use name attributes that match.",
                    "Wrap the label in a <span>.",
                ],
                "answer": "option_2",
                "explanation": "Setting for on the label to the input id creates a programmatic association.",
            },
            {
                "title": "Document Outline",
                "question": "Which tag introduces the main content unique to the page?",
                "options": ["<main>", "<body>", "<article>", "<aside>"],
                "answer": "option_1",
                "explanation": "<main> identifies the central content, improving document outlines and accessibility.",
            },
        ],
    )

    add_group(
        "html",
        "hard",
        [
            {
                "title": "ARIA Roles",
                "question": "Which ARIA role is appropriate for a custom button built with <div>?",
                "options": ["role='link'", "role='button'", "role='menu'", "role='toolbar'"],
                "answer": "option_2",
                "explanation": "role='button' communicates button behavior to assistive technologies on non-semantic elements.",
            },
            {
                "title": "Preloading Resources",
                "question": "Which element is used to preload critical CSS resources?",
                "options": [
                    "<link rel='preload' as='style' href='styles.css'>",
                    "<meta rel='preload' href='styles.css'>",
                    "<script rel='preload' src='styles.css'>",
                    "<style preload href='styles.css'>",
                ],
                "answer": "option_1",
                "explanation": "Using <link rel='preload' as='style'> hints the browser to fetch CSS early.",
            },
            {
                "title": "SVG Accessibility",
                "question": "How should you provide accessible text for inline SVG icons?",
                "options": [
                    "Rely on fill attributes.",
                    "Wrap the SVG in a <p> tag.",
                    "Use <title> and aria-labelledby within the SVG.",
                    "Set width and height attributes only.",
                ],
                "answer": "option_3",
                "explanation": "<title> and aria-labelledby provide descriptive text for assistive tech on SVGs.",
            },
            {
                "title": "Content Security Policy",
                "question": "Which meta tag configures a Content Security Policy?",
                "options": [
                    "<meta http-equiv='Content-Security-Policy' content=\"default-src 'self'\">",
                    "<meta name='csp' value='self'>",
                    "<meta security='self'>",
                    "<meta referrerpolicy='strict-origin'>",
                ],
                "answer": "option_1",
                "explanation": "CSP is defined via the http-equiv Content-Security-Policy meta tag or HTTP headers.",
            },
            {
                "title": "Custom Elements",
                "question": "Which attribute associates a custom element with its shadow DOM template?",
                "options": ["is", "shadow", "slot", "use"],
                "answer": "option_3",
                "explanation": "slot attributes define insertion points for light DOM content within shadow DOM templates.",
            },
        ],
    )

    add_group(
        "python",
        "easy",
        [
            {
                "title": "List Creation",
                "question": "Which syntax correctly creates a list in Python?",
                "options": ["{1, 2, 3}", "(1, 2, 3)", "[1, 2, 3]", "<1, 2, 3>"],
                "answer": "option_3",
                "explanation": "Lists use square brackets [], distinguishing them from tuples () and sets {}.",
            },
            {
                "title": "String Interpolation",
                "question": "Which approach uses an f-string to interpolate variables?",
                "options": [
                    "\"Hello {}\".format(name)",
                    "\"Hello %s\" % name",
                    "f\"Hello {name}\"",
                    "concat(\"Hello\", name)",
                ],
                "answer": "option_3",
                "explanation": "f\"...\" literals interpolate expressions directly using braces.",
            },
            {
                "title": "Boolean Evaluation",
                "question": "What is the output of bool([])?",
                "options": ["True", "False", "None", "Error"],
                "answer": "option_2",
                "explanation": "Empty containers are falsy in Python, so bool([]) evaluates to False.",
            },
            {
                "title": "Dictionary Access",
                "question": "Which method safely retrieves a value with a default from a dict?",
                "options": ["dict['key']", "dict.get('key', default)", "dict.value('key', default)", "dict.fetch('key')"],
                "answer": "option_2",
                "explanation": "get returns None or a provided default without raising KeyError when the key is missing.",
            },
            {
                "title": "Looping Over Range",
                "question": "How many times does for _ in range(3): iterate?",
                "options": ["2", "3", "4", "Indeterminate"],
                "answer": "option_2",
                "explanation": "range(3) produces 0,1,2 resulting in three iterations.",
            },
        ],
    )

    add_group(
        "python",
        "medium",
        [
            {
                "title": "List Comprehension",
                "question": "Which comprehension squares only even numbers from a list nums?",
                "options": [
                    "[n**2 for n in nums if n % 2 == 0]",
                    "[n**2 if n % 2 == 0 in nums]",
                    "{n**2 for n if n % 2 == 0 in nums}",
                    "(n**2 for n in nums) if n % 2 == 0",
                ],
                "answer": "option_1",
                "explanation": "List comprehension with conditional clause filters even numbers before squaring.",
            },
            {
                "title": "Enumerate Usage",
                "question": "What does enumerate(iterable, start=1) return?",
                "options": [
                    "A list of indices only.",
                    "Pairs of (index, value) starting at 1.",
                    "Pairs of (value, index) starting at 0.",
                    "A generator of values only.",
                ],
                "answer": "option_2",
                "explanation": "enumerate yields tuples of index and value, with custom starting index.",
            },
            {
                "title": "Exception Handling",
                "question": "Which block executes whether or not an exception occurs?",
                "options": ["try", "except", "else", "finally"],
                "answer": "option_4",
                "explanation": "The finally block always executes, useful for cleanup logic.",
            },
            {
                "title": "Mutable Default Argument",
                "question": "Why should mutable default arguments generally be avoided?",
                "options": [
                    "They cause syntax errors.",
                    "They are recreated on every call.",
                    "They persist state between calls unexpectedly.",
                    "They slow down function calls.",
                ],
                "answer": "option_3",
                "explanation": "Defaults are evaluated once, causing shared mutable state between invocations.",
            },
            {
                "title": "Decorators",
                "question": "What does a function decorator return?",
                "options": [
                    "Always the original function.",
                    "Functions cannot be returned.",
                    "A new callable that wraps the original function.",
                    "Only class instances.",
                ],
                "answer": "option_3",
                "explanation": "Decorators typically return a wrapper function that can extend behavior.",
            },
        ],
    )

    add_group(
        "python",
        "hard",
        [
            {
                "title": "Generators vs Iterators",
                "question": "What distinguishes a generator function from a regular function?",
                "options": [
                    "Generators cannot accept arguments.",
                    "Generators use yield and return iterators.",
                    "Generators execute faster.",
                    "Generators return lists automatically.",
                ],
                "answer": "option_2",
                "explanation": "A generator yields values lazily and returns an iterator object.",
            },
            {
                "title": "Context Managers",
                "question": "Which protocol methods must a context manager class implement?",
                "options": [
                    "__open__ and __close__",
                    "__enter__ and __exit__",
                    "__start__ and __stop__",
                    "__with__ and __done__",
                ],
                "answer": "option_2",
                "explanation": "__enter__ runs on entering the with block, __exit__ handles cleanup or exceptions.",
            },
            {
                "title": "Metaclasses",
                "question": "What does a metaclass customize in Python?",
                "options": [
                    "Instance attribute lookup only.",
                    "How classes themselves are created.",
                    "The garbage collector behavior.",
                    "Only method resolution order.",
                ],
                "answer": "option_2",
                "explanation": "Metaclasses control class creation allowing custom type construction.",
            },
            {
                "title": "Asyncio Awaitables",
                "question": "Which objects can be awaited inside an async function?",
                "options": ["Only coroutines", "Coroutines, Tasks, or Futures", "Only threads", "Any callable"],
                "answer": "option_2",
                "explanation": "await accepts awaitable objects such as coroutines, Tasks, or Futures.",
            },
            {
                "title": "Descriptor Protocol",
                "question": "Which descriptor method enables write access interception?",
                "options": ["__get__", "__set__", "__delete__", "__call__"],
                "answer": "option_2",
                "explanation": "__set__ allows descriptors to manage attribute assignment operations.",
            },
        ],
    )

    add_group(
        "django",
        "easy",
        [
            {
                "title": "Start a Project",
                "question": "Which command creates a new Django project named mysite?",
                "options": [
                    "django-admin startproject mysite",
                    "django-admin startapp mysite",
                    "python manage.py startproject mysite",
                    "python manage.py createproject mysite",
                ],
                "answer": "option_1",
                "explanation": "django-admin startproject <name> scaffolds a new project structure.",
            },
            {
                "title": "Django App Creation",
                "question": "Which command creates a new Django app named blog?",
                "options": [
                    "python manage.py startapp blog",
                    "django-admin startproject blog",
                    "python manage.py createapp blog",
                    "python manage.py runapp blog",
                ],
                "answer": "option_1",
                "explanation": "startapp initializes a new reusable application within a project.",
            },
            {
                "title": "Model Migration",
                "question": "What command generates migrations for model changes?",
                "options": [
                    "python manage.py migrate",
                    "python manage.py makemigrations",
                    "python manage.py collectstatic",
                    "python manage.py createsuperuser",
                ],
                "answer": "option_2",
                "explanation": "makemigrations inspects models and prepares migration files for schema changes.",
            },
            {
                "title": "URL Configuration",
                "question": "Which function maps URL patterns to view callables?",
                "options": ["path()", "url()", "include()", "reverse()"],
                "answer": "option_1",
                "explanation": "path() defines URL routes paired with views in modern Django versions.",
            },
            {
                "title": "Template Loading",
                "question": "Where should templates be stored for app-level discovery by default?",
                "options": [
                    "app/templates/",
                    "project/static/",
                    "app/static/",
                    "project/media/",
                ],
                "answer": "option_1",
                "explanation": "With APP_DIRS enabled, Django looks for <app>/templates/ for templates.",
            },
        ],
    )

    add_group(
        "django",
        "medium",
        [
            {
                "title": "Generic Views",
                "question": "Which generic view lists objects from a model?",
                "options": [
                    "TemplateView",
                    "DetailView",
                    "ListView",
                    "FormView",
                ],
                "answer": "option_3",
                "explanation": "ListView retrieves object lists and renders them using a context variable.",
            },
            {
                "title": "QuerySet Optimization",
                "question": "Which method prefetches related many-to-many records efficiently?",
                "options": [
                    "select_related()",
                    "prefetch_related()",
                    "defer()",
                    "only()",
                ],
                "answer": "option_2",
                "explanation": "prefetch_related performs additional queries to batch-fetch related objects.",
            },
            {
                "title": "Custom Template Filters",
                "question": "Where do you register a custom template filter?",
                "options": [
                    "forms.py",
                    "admin.py",
                    "templatetags/<module>.py",
                    "views.py",
                ],
                "answer": "option_3",
                "explanation": "Custom filters live inside a templatetags package registered with template.Library().",
            },
            {
                "title": "Class-Based Views URL",
                "question": "How do you reference a class-based view in urls.py?",
                "options": [
                    "path('home/', HomeView, name='home')",
                    "path('home/', HomeView.as_view(), name='home')",
                    "path('home/', HomeView.call(), name='home')",
                    "path('home/', HomeView.view(), name='home')",
                ],
                "answer": "option_2",
                "explanation": "as_view() converts the class into a callable view configured as a URL handler.",
            },
            {
                "title": "Forms Validation",
                "question": "Which method validates and returns cleaned data in a Form?",
                "options": ["form.valid()", "form.clean()", "form.save()", "form.render()"],
                "answer": "option_2",
                "explanation": "clean() aggregates field cleaning and can enforce cross-field validation logic.",
            },
        ],
    )

    add_group(
        "django",
        "hard",
        [
            {
                "title": "Signals",
                "question": "Which signal fires after a model instance is saved?",
                "options": ["pre_save", "post_save", "pre_init", "post_delete"],
                "answer": "option_2",
                "explanation": "post_save is emitted once a model's save() operation completes.",
            },
            {
                "title": "Custom Managers",
                "question": "What should a custom manager inherit from?",
                "options": ["models.Model", "models.Manager", "models.QuerySet", "object"],
                "answer": "option_2",
                "explanation": "Subclassing models.Manager allows custom query helper methods.",
            },
            {
                "title": "Database Transactions",
                "question": "Which decorator wraps a view in an atomic database transaction?",
                "options": [
                    "@transaction.atomic",
                    "@transaction.commit",
                    "@database.atomic",
                    "@models.transaction",
                ],
                "answer": "option_1",
                "explanation": "transaction.atomic ensures all DB operations within the block succeed or rollback.",
            },
            {
                "title": "Custom Authentication Backend",
                "question": "Which method must a custom auth backend implement?",
                "options": ["authenticate()", "authorize()", "grant()", "login()"],
                "answer": "option_1",
                "explanation": "authenticate() receives credentials and returns a user or None.",
            },
            {
                "title": "Caching Framework",
                "question": "How do you access a configured cache named 'default'?",
                "options": [
                    "from django.core.cache import caches; caches['default']",
                    "import cache; cache.default",
                    "settings.CACHES['default']",
                    "Cache.get('default')",
                ],
                "answer": "option_1",
                "explanation": "caches returns configured backends; caches['default'] gives the default Cache object.",
            },
        ],
    )

    return questions


def seed_full_question_set(apps, schema_editor):
    Questions = apps.get_model("Code_Mix", "Questions")
    Options = apps.get_model("Code_Mix", "Options")

    for record in get_question_records():
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


def delete_full_question_set(apps, schema_editor):
    Questions = apps.get_model("Code_Mix", "Questions")
    titles = [record["title"] for record in get_question_records()]
    Questions.objects.filter(title__in=titles).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("Code_Mix", "0023_seed_initial_questions"),
    ]

    operations = [
        migrations.RunPython(seed_full_question_set, delete_full_question_set),
    ]
