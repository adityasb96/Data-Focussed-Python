import sys
import matplotlib.pyplot as plt
import os
import fhirclient.models.bundle as b
import json
from datetime import date


def get_patients(bundle_path):
    filelist = os.listdir(bundle_path)
    Patient_objects = []
    for everyfile in filelist:
        with open(bundle_path + everyfile, 'r') as h:
            js = json.load(h)
            Bundle = b.Bundle(js)
            for e in Bundle.entry:
                if e.request.url == 'Patient':
                    Patient_objects.append(e.resource)
    # print(Patient_objects)
    return Patient_objects

def plot_age_by_gender(bundle_path, figure_name='q1_age_by_gender.png'):
    """17 points for correctness, 3 Points for Style and Efficiency
    See https://briankolowitz.github.io/data-focused-python/individual-project/project-description.html
    Save the figure to a PNG file with the specified figure_name
    Note : you CANNOT use Numpy or Pandas
    Note : you MUST ONLY use matplotlib

    Arguments:
        bundle_path {str} -- path to Synthea generated FHIR bundles
    """

    # Function for Birthdate to age conversion
    def age(born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    # Get patient gender and age
    age_gender = []
    ag = [(p.gender, age(p.birthDate.date)) for p in get_patients(bundle_path)]
    ag = ag + age_gender

    plt.suptitle('Patients by age')

    # Plot Males
    males = [a[1] for a in ag if a[0] == 'male']
    s1 = plt.subplot(1, 2, 1)
    s1.yaxis.tick_right()  # Shift Y axis
    s1.set_yticklabels([])
    s1.title.set_text('Males')
    plt.hist(males, bins=20, color='blue', orientation='horizontal')
    plt.gca().invert_xaxis()
    plt.xlabel('Count')
    # Plot Females
    females = [a[1] for a in ag if a[0] == 'female']
    s2 = plt.subplot(1, 2, 2)
    s2.title.set_text('Females')
    plt.hist(females, bins=20, color='pink', orientation='horizontal')
    plt.xlabel('Count')

    plt.savefig(figure_name, dpi=100)
    plt.show()

def plot_by_gender_and_race(bundle_path, figure_name='q2_by_gender_and_race.png'):
    """17 points for correctness, 3 Points for Style and Efficiency
    See https://briankolowitz.github.io/data-focused-python/individual-project/project-description.html
    Save the figure to a PNG file with the specified figure_name
    Note : you CANNOT use Numpy or Pandas
    Note : you MUST ONLY use matplotlib

    Arguments:
        bundle_path {str} -- path to Synthea generated FHIR bundles
    """

    race = [p.extension[0].extension[0].valueCoding.display for p in get_patients(bundle_path) if p.extension != None]
    gender = [p.gender for p in get_patients(bundle_path)]
    race_gender = list(zip(race, gender))

    rg = { 'female': [], 'male': [] }
    for e in race_gender:
        if e[1] == 'female':
            rg['female'].append(e[0])
        elif e[1] == 'male':
            rg['male'].append((e[0]))

    males = sorted(list(set(rg['male'])))
    females = sorted(list(set(rg['female'])))

    all_x = sorted(list(set(males).union(set(females))))

    male_y = [rg['male'].count(r) for r in all_x]
    female_y = [rg['female'].count(r) for r in all_x]

    width = 0.2
    xm = [x for x in range(len(males))]
    xf = [x + width for x in range(len(females))]
    xc = [x + width / 2 for x in range(len(males))]

    ax = plt.subplot()
    ax.bar(xm, male_y, width, align='center', color='blue')
    ax.bar(xf, female_y, width, align='center', color='pink')

    ax.set_ylabel('Number of Patients')
    ax.set_xticklabels(all_x)
    ax.set_xticks(xc)
    ax.set_title('Patients by Gender and Race')

    ax.legend(['Male', 'Female'], loc=2)

    plt.savefig(figure_name, dpi=100)
    plt.show()


def plot_by_gender_and_birth_country(bundle_path, figure_name='q3_by_gender_and_birth_country.png'):
    """17 points for correctness, 3 Points for Style and Efficiency
    See https://briankolowitz.github.io/data-focused-python/individual-project/project-description.html
    Save the figure to a PNG file with the specified figure_name
    Note : you CANNOT use Numpy or Pandas
    Note : you MUST ONLY use matplotlib

    Arguments:
        bundle_path {str} -- path to Synthea generated FHIR bundles
    """
    gender = [p.gender for p in get_patients(bundle_path)]
    birth_country = [p.extension[4].valueAddress.country for p in get_patients(bundle_path)]
    gender_birth_country = list(zip(gender, birth_country))

    bg = { 'female': [], 'male': [] }
    for e in gender_birth_country:
        if e[0] == 'female':
            bg['female'].append(e[1])
        elif e[0] == 'male':
            bg['male'].append((e[1]))

    males = sorted(list(set(bg['male'])))
    females = sorted(list(set(bg['female'])))
    all_x = sorted(list(set(males).union(set(females))))

    male_y = [bg['male'].count(r) for r in all_x]
    female_y = [bg['female'].count(r) for r in all_x]

    width = 0.2
    xm = [x for x in range(len(all_x))]
    xf = [x + width for x in range(len(all_x))]
    xc = [x + width / 2 for x in range(len(all_x))]

    ax = plt.subplot()
    ax.bar(xm, male_y, width, align='center', color='blue')
    ax.bar(xf, female_y, width, align='center', color='pink')

    ax.set_ylabel('Number of Patients')
    ax.set_xticklabels(all_x)
    ax.set_xticks(xc)
    ax.set_title('Patients by Gender and Birth Country')

    ax.legend(['Male', 'Female'], loc=2)

    plt.savefig(figure_name, dpi=100)
    plt.show()\

def plot_by_gender_and_mortality(bundle_path, figure_name='q4_by_gender_and_mortality.png'):
    """17 points for correctness, 3 Points for Style and Efficiency
    See https://briankolowitz.github.io/data-focused-python/individual-project/project-description.html
    Save the figure to a PNG file with the specified figure_name
    Note : you CANNOT use Numpy or Pandas
    Note : you MUST ONLY use matplotlib

    Arguments:
        bundle_path {str} -- path to Synthea generated FHIR bundles
    """
    gender = [p.gender for p in get_patients(bundle_path)]
    mortality = [True if (hasattr(p, 'deceasedDateTime') and p.deceasedDateTime != None) else False for p in
                 get_patients(bundle_path)]

    gender_mortality = zip(gender, mortality)
    bg = { 'female': [], 'male': [] }
    for e in gender_mortality:
        if e[0] == 'female':
            bg['female'].append(e[1])
        elif e[0] == 'male':
            bg['male'].append((e[1]))

    males = sorted(list(set(bg['male'])))
    females = sorted(list(set(bg['female'])))
    all_x = sorted(list(set(males).union(set(females))))

    male_y = [bg['male'].count(r) for r in all_x]
    female_y = [bg['female'].count(r) for r in all_x]

    width = 0.2
    xm = [x for x in range(len(all_x))]
    xf = [x + width for x in range(len(all_x))]
    xc = [x + width / 2 for x in range(len(all_x))]

    ax = plt.subplot()
    ax.bar(xm, male_y, width, align='center', color='blue')
    ax.bar(xf, female_y, width, align='center', color='pink')

    ax.set_ylabel('Number of Patients')
    ax.set_xticklabels(all_x)
    ax.set_xticks(xc)
    ax.set_title('Patients by Gender and Deceased')

    ax.legend(['Male', 'Female'], loc=1)

    plt.savefig(figure_name, dpi=100)
    plt.show()

def plot_challenge_question_1(bundle_path, figure_name='q6_challenge_question_1.png'):
    """5 Points
    Plot anything you want that uses at least 2 FHIR resources
    Save the figure to a PNG file with the specified figure_name

    Arguments:
        bundle_path {str} -- path to Synthea generated FHIR bundles
    """

    mortality = [True if (hasattr(p, 'deceasedDateTime') and p.deceasedDateTime != None) else False for p in
                 get_patients(bundle_path)]
    race = [p.extension[0].extension[0].valueCoding.display for p in get_patients(bundle_path) if p.extension != None]

    mortality_race = zip(mortality, race)
    bg = { 'True': [], 'False': [] }
    for e in mortality_race:
        if e[0] == False:
            bg['False'].append(e[1])
        elif e[0] == True:
            bg['True'].append((e[1]))

    Trues = sorted(list(set(bg['True'])))
    Falses = sorted(list(set(bg['False'])))
    all_x = sorted(list(set(Trues).union(set(Falses))))
    true_y = [bg['True'].count(r) for r in all_x]
    false_y = [bg['False'].count(r) for r in all_x]

    width = 0.2
    xm = [x for x in range(len(all_x))]
    xf = [x + width for x in range(len(all_x))]
    xc = [x + width / 2 for x in range(len(all_x))]

    ax = plt.subplot()
    ax.bar(xm, true_y, width, align='center', color='red')
    ax.bar(xf, false_y, width, align='center', color='green')

    ax.set_ylabel('Number of Patients')
    ax.set_xticklabels(all_x)
    ax.set_xticks(xc)
    ax.set_title('Deceased by Race')

    ax.legend(['True', 'False'], loc=2)

    plt.savefig(figure_name, dpi=100)
    plt.show()

def plot_challenge_question_2(bundle_path, figure_name='q7_challenge_question_2.png'):
    """5 Points
    Plot anything you want that uses at least 2 FHIR resources
    Save the figure to a PNG file with the specified figure_name

    Arguments:
        bundle_path {str} -- path to Synthea generated FHIR bundles
    """
    mortality = [True if (hasattr(p, 'deceasedDateTime') and p.deceasedDateTime != None) else False for p in
                 get_patients(bundle_path)]

    birth_country = [p.extension[4].valueAddress.country for p in get_patients(bundle_path)]

    mortality_birth_country = zip(mortality, birth_country)
    bg = { 'True': [], 'False': [] }
    for e in mortality_birth_country:
        if e[0] == False:
            bg['False'].append(e[1])
        elif e[0] == True:
            bg['True'].append((e[1]))

    Trues = sorted(list(set(bg['True'])))
    Falses = sorted(list(set(bg['False'])))
    all_x = sorted(list(set(Trues).union(set(Falses))))
    true_y = [bg['True'].count(r) for r in all_x]
    false_y = [bg['False'].count(r) for r in all_x]

    width = 0.2
    xm = [x for x in range(len(all_x))]
    xf = [x + width for x in range(len(all_x))]
    xc = [x + width / 2 for x in range(len(all_x))]

    ax = plt.subplot()
    ax.bar(xm, true_y, width, align='center', color='red')
    ax.bar(xf, false_y, width, align='center', color='green')

    ax.set_ylabel('Number of Patients')
    ax.set_xticklabels(all_x)
    ax.set_xticks(xc)
    ax.set_title('Deceased by Birth Country')

    ax.legend(['True', 'False'], loc=2)
    plt.savefig(figure_name, dpi=100)
    plt.show()




# do not modify below this line

if __name__ == "__main__":
    # bundle_path = sys.argv[1]
    bundle_path = "/synthea/output/fhir/"
    plot_age_by_gender(bundle_path)
    plot_by_gender_and_race(bundle_path)
    plot_by_gender_and_birth_country(bundle_path)
    plot_by_gender_and_mortality(bundle_path)
    plot_challenge_question_1(bundle_path)
    plot_challenge_question_2(bundle_path)



