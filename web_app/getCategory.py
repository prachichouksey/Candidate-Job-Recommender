# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 16:21:34 2019

@author: prach
"""
def programmingScore(resume, jdTxt, progWords = None):
    skill_weightage = 40
    skill_threshold = 5
    fout = open("results.tex", "a")
    fout.write("\\textbf{Programming Languages:} \\\\\n")
    
    if(progWords == None):
        programming = ["assembly", "bash", " c " "c++", "c#", "coffeescript", "emacs lisp",
         "go!", "groovy", "haskell", "java", "javascript", "matlab", "max MSP", "objective c", 
         "perl", "php","html", "xml", "css", "processing", "python", "ruby", "sml", "swift", 
         "latex" "unity", "unix" "visual basic" "wolfram language", "xquery", "sql", "node.js", 
         "scala", "kdb", "jquery", "mongodb", "CMMI", "ISO", "finance", "Banking", "Finacle", "Oracle Flexcube", "Fiserv", 
         "TCS BaNcs", "FIS Profile"]
    else:
        programming = progWords
    programmingTotal = 0
    
    jdSkillCount = 0
    jdSkillMatched = []
    for i in range(len(programming)):
        if programming[i].lower() in jdTxt.lower() != -1:
            jdSkillCount += 1
            jdSkillMatched.append(programming[i].lower())
    
    individualSkillWeightage = 0
    
    if( jdSkillCount > 0):
        individualSkillWeightage = skill_weightage/jdSkillCount
    
    ResumeProgrammingSkillsMatchedWithJD = []
    for i in range(len(jdSkillMatched)):
        if jdSkillMatched[i].lower() in resume.lower() != -1:
            programmingTotal += 1
            ResumeProgrammingSkillsMatchedWithJD.append(jdSkillMatched[i].lower())
            if not("#" in jdSkillMatched[i]):
                fout.write(jdSkillMatched[i]+", ")
    
    resumeCorpus = resume.split()
    resumeCorpus = [x.lower() for x in resumeCorpus if isinstance(x, str)]
    jdSkillMatched = [x.lower() for x in jdSkillMatched if isinstance(x, str)]
    list1 = jdSkillMatched
    list2 = resumeCorpus
    results = {}
    for i in list1:
        results[i] = list2.count(i) 
    
    constantValue = (individualSkillWeightage/skill_threshold)
    
    results.update({n: constantValue * results[n] for n in results.keys()})
   
    TotalScore = sum(results.values())
   
    fout.close()
    return TotalScore

def NonTechnicalSkillScore(resume, jd_txt, progWords = None):
    skill_weightage = 5
    skill_threshold = 5
    fout = open("results.tex", "a")
    fout.write("\\textbf{Programming Languages:} \\\\\n")
    
    if(progWords == None):
        NonTechnicalSkill = ["Self-directed learning", "Collaboration", "Communication", "Resilience", "Big-picture mindset", "Prioritization ", "Creativity ",
         "creative", "Insight", "curiosity", "curious", "Openness", "Teamwork", "Time management", "Emotional intelligence", 
         "quick learner", "problem solver","Customer-service skills", "Planning and organizing", "innovative", "Thinking innovatively and creatively", "Resourceful", "Flexible", "Able to manage own time", "Having self-esteem", 
         "Innovation skills", "Enterprise skills", "Civic or citizenship knowledge and skills", "Sociability", "Self-management", "Integrity", "Honesty", "Human resources", 
         "Participates as a team member", "Works with diversity", "Exercises leadership", "leadership", "Exercises leadership", "Monitors and corrects performance", "Understands systems"]
    else:
        NonTechnicalSkill = progWords
    programmingTotal = 0
    
    jdSkillCount = 0
    jdSkillMatched = []
    for i in range(len(NonTechnicalSkill)):
        if NonTechnicalSkill[i].lower() in jd_txt.lower() != -1:
            jdSkillCount += 1
            jdSkillMatched.append(NonTechnicalSkill[i].lower())
    
    if (jdSkillCount > 0):
        individualSkillWeightage = skill_weightage/jdSkillCount
    else :
        individualSkillWeightage = 0

    ResumeProgrammingSkillsMatchedWithJD = []
    for i in range(len(jdSkillMatched)):
        if jdSkillMatched[i].lower() in resume.lower() != -1:
            programmingTotal += 1
            ResumeProgrammingSkillsMatchedWithJD.append(jdSkillMatched[i].lower())
            if not("#" in jdSkillMatched[i]):
                fout.write(jdSkillMatched[i]+", ")
    
    resumeCorpus = resume.split()
    """ Modify below """
    resumeCorpus = resumeCorpus + ResumeProgrammingSkillsMatchedWithJD
    resumeCorpus = [x.lower() for x in resumeCorpus if isinstance(x, str)]
    jdSkillMatched = [x.lower() for x in jdSkillMatched if isinstance(x, str)]
    
    print("jd skills matched in lower case",jdSkillMatched)
    list1 = jdSkillMatched
    list2 = resumeCorpus
    results = {}
    for i in list1:
        if list2.count(i) > skill_threshold:
           results[i] = skill_threshold
        else:
           results[i] = list2.count(i)
    print("Dictionary from resume is ",results)
    constantValue = (individualSkillWeightage/skill_threshold)
    results.update({n: constantValue * results[n] for n in results.keys()})
    print("updated dict is ", results)

    TotalScore = sum(results.values())
    print("Score is ", TotalScore)

    fout.close()
    return TotalScore
