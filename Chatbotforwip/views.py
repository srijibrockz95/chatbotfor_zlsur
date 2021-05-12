from flask import *
from sqlalchemy import desc, or_
from sqlalchemy.sql.operators import isnot
from .models import Login, QuestionAnswer, Booking
from . import db
from werkzeug.security import check_password_hash
from fpdf import FPDF
import datetime
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

auth = Blueprint('auth', __name__)


def makepdf(filename, filecontent):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.set_fill_color(35, 107, 142)
    pdf.cell(0, 5, txt="Date: "+str(datetime.date.today()),
             ln=2, align='R')
    pdf.cell(0, 10, txt="ABB - Appointment Booking Bot",
             ln=4, align='C', fill=True)
    pdf.cell(50, 10, txt="    "+filecontent,
             ln=10, align='L')
    pdf.cell(0, 10, txt="*******************************",
             ln=15, align='C')
    pdf.output("Chatbotforwip/static/" + filename)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/')
def index():
    try:
        if 'userid' in session and session['loggedin'] is True:
            if request.args.get('msg') != '':
                flash(request.args.get('msg'))
            if request.args.get('questions') is not None and request.args.get('questions') != '':
                questions = request.args.get('questions')
                questions = json.loads(questions)
            else:
                questions = None
            if request.args.get('otherques') is not None and request.args.get('otherques') != '':
                otherques = request.args.get('otherques')
                otherques = json.loads(otherques)
            else:
                otherques = None
            if request.args.get('foundques') is not None and request.args.get('foundques') != '':
                foundques = request.args.get('foundques')
                foundques = json.loads(foundques)
            else:
                foundques = None
            return render_template('index.html', fullname=str(session['userfname']).split(" ")[0],
                                   greetings=request.args.get('openningques') if request.args.get('openningques') is not
                                   None else '' if "openques" not in session else session["openques"]
                                   if session["openques"] is not None else '',
                                   questions=questions['questions'] if questions
                                   is not None else '' if "questions" not in session
                                   else json.loads(session['questions'])["questions"] if session['questions'] is
                                   not None else '',
                                   chosenquesans=request.args.get('chosenquesans') if request.args.get(
                                       'chosenquesans') is not None else '' if "chosenquesans" not in session
                                   else session["chosenquesans"] if session["chosenquesans"] is
                                   not None else '',
                                   datereqd=request.args.get('datereqd') if "datereqd" not in session
                                   else session["datereqd"],
                                   filepth=request.args.get('filepth') if "filepth" not in session
                                   else session["filepth"],
                                   typecustomques=request.args.get('typecustomques') if "typecustomques" not in session
                                   else session["typecustomques"],
                                   otherques=otherques['otherquestions'] if otherques is not None else ''
                                   if 'otherques' not in session
                                   else json.loads(session['otherques'])["otherquestions"] if session['otherques'] is
                                   not None else '',
                                   chosenques=request.args.get('chosenques') if request.args.get('chosenques') is not
                                   None else '' if "chosenques" not in session
                                   else session["chosenques"] if session["chosenques"] is
                                   not None else '',
                                   foundques=foundques['foundquestions'] if foundques is not None else ''
                                   if 'foundques' not in session
                                   else json.loads(session['foundques'])["foundquestions"] if session['foundques'] is
                                   not None else '')
        else:
            session.pop('loggedin', None)
            session.pop('userid', None)
            session.pop('userfname', None)
            session.pop('questions', None)
            session.pop('openques', None)
            session.pop('datereqd', None)
            session.pop('chosenquesans', None)
            session.pop('filepth', None)
            session.pop('typecustomques', None)
            session.pop('chosenques', None)
            session.pop('otherques', None)
            session.pop('foundques', None)
            flash('Successfully logged out.')
            return redirect(url_for('auth.login'))
    except Exception as e:
        print(e)
        flash('Error')
        return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    try:
        questions = []
        if request.method == "POST":
            if 'username' in request.form and 'password' in request.form:
                username = request.form['username']
                password = request.form['password']
                userdet = Login.query.filter_by(useremail=username).first()
                if userdet:
                    if check_password_hash(userdet.passwordhash, password):
                        session.permanent = True
                        session['loggedin'] = True
                        session['userid'] = userdet.userid
                        session['userfname'] = userdet.userfname
                        greet = QuestionAnswer.query.filter_by(question_type='Introduction') \
                            .order_by(desc(QuestionAnswer.creationdatetime))
                        if greet.first() is not None:
                            openques = greet.first().question
                        else:
                            openques = None
                        queslist = QuestionAnswer.query.order_by(desc(QuestionAnswer.orderofdisp)) \
                            .filter(QuestionAnswer.answer.isnot(None))
                        if queslist.first() is not None:
                            for q in queslist:
                                qdata = QuestionAnswer.query.filter_by(id=q.id)
                                if '?' in qdata.first().question:
                                    questions.append(qdata.first().question)
                            questions = list(set(questions))
                        else:
                            questions = ''
                        questions = json.dumps({"questions": questions})
                        session["questions"] = questions
                        session["openques"] = openques
                        session["datereqd"] = None
                        session["chosenquesans"] = None
                        session["filepth"] = None
                        session["typecustomques"] = None
                        session["otherques"] = None
                        session["chosenques"] = None
                        session["foundques"] = None
                        return redirect(url_for('auth.index', openningques=str(openques), questions=questions))
                    else:
                        flash('Incorrect credentials !!')
                        return redirect(url_for('auth.login'))
                else:
                    flash('User does not exist !!')
                    return redirect(url_for('auth.login'))
            else:
                flash('Please provide email and password to login.')
                return redirect(url_for('auth.login'))
    except Exception as e:
        print(e)
        flash('Error')
        return redirect(url_for('auth.login'))


@auth.route('/submitchoseques', methods=['POST'])
def submitchoseques():
    try:
        ques = []
        otherques = []
        foundques = []
        datereqd = None
        answer = None
        filename = None
        invalid = False
        msg = ""
        if request.method == "POST":
            chosenques = ''
            for i in request.form:
                chosenques = i
            findnextques = QuestionAnswer.query.filter_by(question=chosenques).first()
            if findnextques:
                if chosenques == "Submit":
                    if 'customques' in request.form:
                        if request.form['customques'] is not None:
                            cq = request.form['customques']
                            if cq != '':
                                existing_ques = QuestionAnswer.query.filter(QuestionAnswer.question == cq).one_or_none()
                                if existing_ques is None:
                                    answer = findnextques.answer
                                    stop_words = set(stopwords.words('english'))
                                    tokenizer = RegexpTokenizer(r'\w+')
                                    word_tokens = tokenizer.tokenize(cq)
                                    filtered_sentence = [w for w in word_tokens if w not in stop_words]
                                    for fs in filtered_sentence:
                                        queslist = QuestionAnswer.query.filter(or_(QuestionAnswer.question_type ==
                                                                                   fs.title(),
                                                                                   QuestionAnswer.question.contains(
                                                                                       fs)),
                                                                               QuestionAnswer.answer.isnot(None))
                                        if queslist.first() is not None:
                                            for q in queslist:
                                                if '?' in q.question:
                                                    foundques.append(q.question)
                                    foundques = list(set(foundques))
                                    customquesins = QuestionAnswer("Others Questions", cq, None, None, None,
                                                                   session['userid'])
                                    db.session.add(customquesins)
                                    db.session.commit()
                                else:
                                    invalid = True
                                    msg = "Your query already exists."
                            else:
                                invalid = True
                                msg = "Please enter your query"
                if chosenques == "Submit the date.":
                    if 'appointdt' in request.form:
                        if request.form['appointdt'] is not None:
                            date = request.form['appointdt']
                            if date != '':
                                answer = findnextques.answer
                                if date >= datetime.date.today().strftime('%Y-%m-%d'):
                                    bookingmessage = date
                                    bookins = Booking(session['userid'], bookingmessage, session['userid'])
                                    db.session.add(bookins)
                                    db.session.commit()
                                else:
                                    invalid = True
                                    msg = "Please select valid date, today or any date thereafter."
                            else:
                                invalid = True
                                msg = "Please enter the date"
                if chosenques == "Do you want to know your appointment booking status?":
                    answer = findnextques.answer
                    bookingdet = Booking.query.filter_by(userid=session['userid']) \
                        .order_by(desc(Booking.id))
                    if bookingdet.first() is not None:
                        if 'Hi' in bookingdet.first().bookingmessage:
                            bookingmessage = bookingdet.first().bookingmessage
                        else:
                            bookingmessage = "Hi " + session['userfname'] + ", " + answer + \
                                             bookingdet.first().bookingmessage + "."
                        bookingdet.first().bookingmessage = bookingmessage
                        db.session.add(bookingdet.first())
                        db.session.commit()
                        bookingdet = Booking.query.filter_by(userid=session['userid']) \
                            .order_by(desc(Booking.id))
                        if bookingdet.first() is not None:
                            answer = bookingdet.first().bookingmessage
                    else:
                        invalid = True
                        msg = "You don't have any previous appointments. Please first book an appointment."
                if chosenques == "Do you want to download appointment booking report?":
                    bookingdet = Booking.query.filter_by(userid=session['userid']) \
                        .order_by(desc(Booking.id))
                    if bookingdet.first() is not None:
                        if 'Hi' in bookingdet.first().bookingmessage:
                            bookingmessage = bookingdet.first().bookingmessage
                        else:
                            bookingmessage = "Hi " + session['userfname'] + ", " + "Your " \
                                                                                   "appointment " \
                                                                                   "booking is confirmed on " \
                                             + bookingdet.first().bookingmessage + "."
                        bookingdet.first().bookingmessage = bookingmessage
                        db.session.add(bookingdet.first())
                        db.session.commit()
                        filecontent = bookingdet.first().bookingmessage
                        filename = str(session['userfname']) + "_Booking_Report_" + str(
                            datetime.datetime.now().replace(microsecond=0)).replace('-', '_').replace(" ", "_") \
                            .replace(':', '_') + ".pdf"
                        makepdf(filename, filecontent)
                        answer = findnextques.answer
                    else:
                        invalid = True
                        msg = "You don't have any previous appointments. Please first book an appointment."
                if chosenques == "Others?":
                    answer = findnextques.answer
                    typecustomques = 1
                else:
                    typecustomques = None
                # region below is the block of code to fetch list of questions
                queslist = QuestionAnswer.query.order_by(desc(QuestionAnswer.orderofdisp)) \
                    .filter(QuestionAnswer.answer.isnot(None))
                if queslist.first() is not None:
                    for q in queslist:
                        qdata = QuestionAnswer.query.filter_by(id=q.id)
                        if '?' in qdata.first().question:
                            otherques.append(qdata.first().question)
                    otherques = list(set(otherques))
                if findnextques.relatedquesid is not None:
                    relatedqdata = QuestionAnswer.query.filter_by(id=findnextques.relatedquesid)
                    if relatedqdata.first() is not None:
                        if relatedqdata.first().question in otherques:
                            otherques.remove(relatedqdata.first().question)
                        if 'date' in relatedqdata.first().question:
                            datereqd = 1
                        else:
                            datereqd = None
                    else:
                        datereqd = None
                    if '?' in relatedqdata.first().question or 'date' in relatedqdata.first().question:
                        ques.append(relatedqdata.first().question)
                if len(foundques) > 0:
                    for element in foundques:
                        if element in otherques:
                            otherques.remove(element)
                    if len(ques) > 0:
                        for element in foundques:
                            if element in ques:
                                ques.remove(element)
                questions = json.dumps({"questions": ques})
                otherquestions = json.dumps({"otherquestions": otherques})
                foundquestions = json.dumps({"foundquestions": foundques})
                ques.clear()
                otherques.clear()
                foundques.clear()
                chosenques = chosenques if '?' in chosenques else 'Submitted'
                # end region
                if invalid is False:
                    session["questions"] = questions
                    session["datereqd"] = datereqd
                    session["chosenquesans"] = answer
                    session["filepth"] = filename
                    session["typecustomques"] = typecustomques
                    session["otherques"] = otherquestions
                    session["chosenques"] = chosenques
                    session["foundques"] = foundquestions
                    session.pop('openques', None)
                    return redirect(url_for('auth.index', questions=questions, datereqd=datereqd,
                                            chosenquesans=answer, otherques=otherquestions,
                                            filepth=filename, typecustomques=typecustomques, msg=msg,
                                            chosenques=chosenques,
                                            foundques=foundquestions))
                else:
                    return redirect(url_for('auth.index', questions=session["questions"], datereqd=session["datereqd"],
                                            chosenquesans=session["chosenquesans"], otherques=session["otherques"],
                                            filepth=session["filepth"], typecustomques=session["typecustomques"],
                                            msg=msg, chosenques=session["chosenques"],
                                            foundques=session["foundques"]))
    except Exception as e:
        print(e)
        return redirect(url_for('auth.index', msg='Error'))


@auth.route('/logout')
def logout():
    try:
        if session['loggedin'] is True:
            session.pop('loggedin', None)
            session.pop('userid', None)
            session.pop('userfname', None)
            session.pop('questions', None)
            session.pop('openques', None)
            session.pop('datereqd', None)
            session.pop('chosenquesans', None)
            session.pop('filepth', None)
            session.pop('typecustomques', None)
            session.pop('chosenques', None)
            session.pop('otherques', None)
            session.pop('foundques', None)
            flash('Successfully logged out.')
            return redirect(url_for('auth.login'))
    except Exception as e:
        print(e)
        return redirect(url_for('auth.login', msg='Error'))
