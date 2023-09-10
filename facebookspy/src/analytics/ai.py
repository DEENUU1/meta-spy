from langchain import PromptTemplate, HuggingFaceHub, LLMChain
from dotenv import load_dotenv
from ..repository import (
    event_repository,
    family_member_repository,
    group_repository,
    like_repository,
    person_repository,
    place_repository,
    post_repository,
    recent_place_repository,
    review_repository,
    work_education_repository,
)
from typing import Tuple, List
from rich import print as rprint

load_dotenv()

TEMPLATE = """Question: {data}


Answer: 
    "Below is an instruction that describes a task. Write a response that appropriately completes the request.
    \n\n### Instruction:\n 
    Evaluate a person based on provided data. 
    The data contains information from various categories, such as personal information, family relationships, friends, places, education and work, recent places, reviews, posts, likes, groups, and events.
    Please provide an assessment or insights about this individual, taking into account their Facebook activity, social interactions, and other available information. 
    You can also offer suggestions regarding this person's profile based on the provided data.
    It's worth noting that these data may be limited or incomplete, so the assessment should be based on the available information.
    Please provide as much detail as possible about the individual's characteristics and any areas that may be worth exploring or evaluating.

    \n\n### Response:"


"""
PROMPT = PromptTemplate(template=TEMPLATE, input_variables=["data"])
llm_chain = LLMChain(
    prompt=PROMPT,
    llm=HuggingFaceHub(
        repo_id="WizardLM/WizardCoder-Python-34B-V1.0", model_kwargs={"temperature": 1}
    ),
)


def format_person_data(person_id: str) -> Tuple[List]:
    """
    Get data for specified Person from models and return formated data
    """
    person = person_repository.get_person(person_id)

    events = event_repository.get_events_by_person(person.id)
    events_data = "\n".join([f"- {event.name} " for event in events])

    family_members = family_member_repository.get_family_member_list(person.id)
    family_members_data = "\n".join(
        [
            f"- {family_member.full_name} ({family_member.role})"
            for family_member in family_members
        ]
    )

    groups = group_repository.get_groups_by_person(person.id)
    groups_data = "\n".join([f"- {group.name} " for group in groups])

    likes = like_repository.get_likes_by_person(person.id)
    likes_data = "\n".join([f"- {like.name} " for like in likes])

    places = place_repository.get_places_list(person.id)
    places_data = "\n".join([f"- {place.name} {place.date} " for place in places])

    posts = post_repository.get_posts_by_person(person.id)
    posts_data = "\n".join(
        [
            f"- Content: {posts.content}, Number of likes: {posts.number_of_likes}, Number of comments: {posts.number_of_comments}, Number of shares: {posts.number_of_shares}  "
            for posts in posts
        ]
    )

    recent_places = recent_place_repository.get_recent_places_list(person.id)
    recent_places_data = "\n".join(
        [
            f"- {recent_place.localization} {recent_place.date} "
            for recent_place in recent_places
        ]
    )

    reviews = review_repository.get_reviews_by_person(person.id)
    reviews_data = "\n".join(
        [f"- {review.company} {review.review} " for review in reviews]
    )

    work_and_education = work_education_repository.get_work_and_education_list(
        person.id
    )
    work_and_education_data = "\n".join(
        [f"- {work_and_education.name} " for work_and_education in work_and_education]
    )

    return (
        person,
        events_data,
        family_members_data,
        groups_data,
        likes_data,
        places_data,
        posts_data,
        recent_places_data,
        reviews_data,
        work_and_education_data,
    )


def get_person_summary(person_id: str) -> None:
    """
    Generate summary using AI model for specified Person object
    """

    rprint(f"[bold green]Start generating summary for person: {person_id}[/bold green]")
    rprint("[bold]Step 1 of 3 - Extract data from models[/bold]")

    (
        person,
        events_data,
        family_members_data,
        groups_data,
        likes_data,
        places_data,
        posts_data,
        recent_places_data,
        reviews_data,
        work_and_education_data,
    ) = format_person_data(person_id)

    t = f"""

    Full name: {person.full_name}
    Email: {person.email}
    Phone number: {person.phone_number}
    Number of friends: {person.number_of_friends}

    Events:
    {events_data}

    Family member:
    {family_members_data}

    Groups:
    {groups_data}

    Likes:
    {likes_data}

    Places:
    {places_data}

    Posts:
    {posts_data}

    Recent places:
    {recent_places_data}

    Reviews:
    {reviews_data}

    Work and education:
    {work_and_education_data}

    """

    rprint("[bold]Step 2 of 3 - Generate summary[/bold]")
    summary = llm_chain.run(t)

    rprint("[bold]Step 3 of 3 - Saving summary to Person object[/bold]")
    person_repository.update_ai_summary(person.id, summary)
    print(summary)
