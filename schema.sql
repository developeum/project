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

create table events (
    id          serial not null,
    event_time  timestamp with time zone,
    city        serial not null,
    description text,
    place       varchar(64),
    logo_path   varchar(128),
    constraint events_pk
        primary key (id),
    constraint events_cities_id_fk
        foreign key (city) references cities
);

create table users (
    id          serial not null,
    email       varchar(64),
    password    char(60),
    phone       varchar(24),
    first_name  varchar(20),
    last_name   varchar(20),
    status      serial not null,
    profile_img varchar(128),
    city        serial not null,
    constraint users_pk
        primary key (id),
    constraint users_statuses_id_fk
        foreign key (status) references statuses,
    constraint users_cities_id_fk
        foreign key (city) references cities
);

create table favorites (
    user_id  serial not null,
    event_id serial not null,
    constraint favorites_pk
        primary key (user_id, event_id),
    constraint favorites_users_id_fk
        foreign key (user_id) references users,
    constraint favorites_events_id_fk
        foreign key (event_id) references events
);

create table user_stack_links (
    user_id  serial not null,
    stack_id serial not null,
    constraint user_stack_links_pk
        primary key (user_id, stack_id),
    constraint user_stack_links_users_id_fk
        foreign key (user_id) references users,
    constraint user_stack_links_stacks_id_fk
        foreign key (stack_id) references stacks
);
