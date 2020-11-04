create table cities (
    id   serial not null,
    city varchar(64),
    constraint cities_pk
        primary key (id)
);

create table statuses (
    id     serial not null,
    status varchar(32),
    constraint statuses_pk
        primary key (id)
);

create table stacks (
    id    serial not null,
    stack varchar(64),
    constraint stacks_pk
        primary key (id)
);

create table categories (
    id       serial not null,
    category varchar(64),
    constraint categories_pk
        primary key (id)
);

create table event_types (
    id         serial not null,
    event_type varchar(32),
    constraint event_types_pk
        primary key (id)
);

create table events (
    id          serial not null,
    name        varchar(128),
    event_type  integer not null default 1,
    event_time  timestamp with time zone,
    city        integer not null default 1,
    place       varchar(256),
    source_url  varchar(256),
    description text,
    logo_path   varchar(256),
    constraint events_pk
        primary key (id),
    constraint events_cities_id_fk
        foreign key (city) references cities,
    constraint events_event_types_id_fk
        foreign key (event_type) references event_types
);

create table users (
    id          serial not null,
    email       varchar(64),
    password    char(60),
    phone       varchar(24),
    first_name  varchar(20),
    last_name   varchar(20),
    status      integer not null default 1,
    profile_img varchar(256),
    city        integer not null default 1,
    constraint users_pk
        primary key (id),
    constraint users_statuses_id_fk
        foreign key (status) references statuses,
    constraint users_cities_id_fk
        foreign key (city) references cities
);

create table user_visit_links (
    user_id     integer not null,
    event_id    integer not null,
    visit_time  timestamp,
    constraint visited_pk
        primary key (user_id, event_id),
    constraint visited_users_id_fk
        foreign key (user_id) references users,
    constraint visited_events_id_fk
        foreign key (event_id) references events
);

create table user_stack_links (
    user_id  integer not null,
    stack_id integer not null,
    constraint user_stack_links_pk
        primary key (user_id, stack_id),
    constraint user_stack_links_users_id_fk
        foreign key (user_id) references users,
    constraint user_stack_links_stacks_id_fk
        foreign key (stack_id) references stacks
);

create table event_category_links (
    event_id    integer not null,
    category_id integer not null,
    constraint event_category_links_pk
        primary key (event_id, category_id),
    constraint event_category_links_events_id_fk
        foreign key (event_id) references events,
    constraint event_category_links_categories_id_fk
        foreign key (category_id) references categories
);

insert into cities (city) values
    ('Не указан'),
    ('Москва'),
    ('Санкт-Петербург');

insert into statuses (status) values
    ('Не указан'),
    ('Студент'),
    ('Трудоустроен');

-- TODO: merge stacks and categories
insert into stacks (stack) values
    ('Веб-разработка'),
    ('Мобильная разработка'),
    ('Data Science'),
    ('QA'),
    ('DevOps'),
    ('Бизнес'),
    ('Прочее');

insert into categories (category) values
    ('Веб-разработка'),
    ('Мобильная разработка'),
    ('Data Science'),
    ('QA'),
    ('DevOps'),
    ('Бизнес'),
    ('Прочее');

insert into event_types (event_type) values
    ('Прочее'),
    ('Хакатон'),
    ('Вебинар'),
    ('Конференция'),
    ('Тренинг'),
    ('Курс'),
    ('Митап'),
    ('Олимпиада');
