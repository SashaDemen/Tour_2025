import datetime
from functools import wraps


from config import app, templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Form, Depends, File, Response, UploadFile


from sqlalchemy.orm import Session


from db import get_db, User, Tour, Buy
from const import TOUR_HTML


@app.get('/', response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):                             # параметр, щоб дістати щось з бд
    tours = db.query(Tour).all()
    user = db.query(User).get(1) # add user to admin
    user.is_admin = True
    db.commit()
    return templates.TemplateResponse('index.html', {'tours': tours, 'request': request})


@app.post('/login')
async def login(request: Request,
                email: str = Form(),
                password: str = Form(),
                db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=email, password=password).first()             #коли користувач авторизується, ми перевіряємо його данні
    if user is None:
        return RedirectResponse(url='/login?after_fail=True', status_code=302)          # якщо вони не вірні, ми перезавантажуємо користувача на ту саму сторінку але передаємо
                                                                                        # query параметрякий буде нам сигналізувати про те, що це не просто завантаження сторінки, а саме
                                                                                        # після невдалої авторизації.
    # якщо дані введені вірно, то записуємо в сесію:
    request.session['user_id'] = user.id                                                # айді користувача для використання його в інших функціоналах
    request.session['is_auth'] = True                                                   # значення яке нам каже що користувач зараз авторизований
    return RedirectResponse('/', status_code=303)


@app.get('/login', response_class=HTMLResponse)
def login(request: Request, after_fail: bool = False):
    context = {'request': request}
    if after_fail:
        context['message'] = 'Email or password is not correct'
    return templates.TemplateResponse('login.html', context)


@app.get('/logout', response_class=HTMLResponse) # функція, щоб користувач вийшов з облікового запису
def logout(request: Request):
    del request.session['user_id']               # видаляємо айді користувача
    request.session['is_auth'] = False           # записуємо значення False
    return RedirectResponse('/', status_code=303)


def login_required(view):                                           # Для перевірки користувача на авторизованість
    @wraps(view)                                                    # реалізуємо свій декоратор для наших ендпоінтів
    async def wrap(request: Request,  *args, **kwargs):             # буде приймати ендпоінт сторінки в якості параметра
        if not request.session.get('is_auth', False):               # перевіряти в данних сесії чи авторизований користувач
            return RedirectResponse('/login', status_code=303)      # якщо так - то просто далі викличе сам ендпоінт
        return await view(request, *args, **kwargs)                 # протилежному випадку - редірект на сторінку авторизації.
    return wrap


@app.post('/create-tour')
@login_required   # користувач обов'язково повинен бути зареєстрованим, щоб зайти на цю сторінку
async def create_tour(
                request: Request,
                name: str = Form(),
                city: str = Form(),
                days: int = Form(),
                price: int = Form(),
                date: str = Form(),
                images: UploadFile = File(),
                db: Session = Depends(get_db)):
    # беремо поточного юзера і ставимо умову:
    user = db.query(User).get(request.session['user_id'])
    if not user.is_admin:
        return RedirectResponse('/login', status_code=303)
    date = datetime.datetime.strptime(date, '%Y-%m-%d', )
    tour = Tour(name=name, city=city, days=days, price=price, date=date)
    db.add(tour)
    db.commit()
    db.refresh(tour)
    with open(f'static/images/{tour.id}.jpg', 'wb') as image:

        content = await images.read()
        image.write(content)
        tour.images = f'/static/images/{tour.id}.jpg'
        db.commit()
        db.refresh(tour)
    return {'id': tour.id}


@app.get('/register', response_class=HTMLResponse)      # реєстрація для користувачів
def reg(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse('register.html', {'users': users, 'request': request})


@app.post('/register')
def register(request: Request, username: str = Form(),
             email: str = Form(),
             password: str = Form(),
             db: Session = Depends(get_db)):  # параметр, щоб дістати щось з бд
    user = User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return RedirectResponse('/', status_code=303)


@app.get('/buy', response_class=HTMLResponse)
@login_required
def buy(request: Request, db: Session = Depends(get_db)):  # проверка авторизации
    tours = db.query(Tour).all()
    return templates.TemplateResponse('index.html', {'tours': tours, 'request': request})


@app.post('/buy-tour')
@login_required
def buy_tour(request: Request, user_id: int = Form(), tour_id: int = Form(),
             start_at: str = Form(), end_at: str = Form(), db: Session = Depends(get_db)):
    start_at = datetime.datetime.strptime(start_at, '%Y-%m-%d')  # преобразуем дату в формат datetime
    end_at = datetime.datetime.strptime(end_at, '%Y-%m-%d')

    # Создаем покупку
    buy = Buy(user_id=user_id, tour_id=tour_id, start_at=start_at, end_at=end_at)
    db.add(buy)
    db.commit()
    db.refresh(buy)

    # Перенаправляем на главную страницу или страницу с туром
    return RedirectResponse(url=f"/tour/{tour_id}", status_code=303)


@app.post('/search')
def search(search:str = Form(),  db: Session = Depends(get_db)):
    tours = db.query(Tour).filter(Tour.name.ilike(f"%{search}%"))
    result = ""
    for tour in tours:                                          # перебираємо всі тури
        result += TOUR_HTML.format(tour_id=tour.id,             # конст зміннна де зберігаються штмл код тура
                                   tour_name=tour.name,
                                   tour_city=tour.city,
                                   tour_days=tour.days,
                                   tour_price=tour.price,
                                   tour_date=tour.date,
                                   tour_images=tour.images)
    return {'tours': result}


@app.get('/tour/{tour_id}', response_class=HTMLResponse)
def tour_details(request: Request, tour_id: int, db: Session = Depends(get_db)):
    tour = db.query(Tour).get(tour_id)
    if not tour:
        return RedirectResponse(url='/', status_code=404)

    return templates.TemplateResponse('tour_details.html', {'request': request, 'tour': tour})
