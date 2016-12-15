create view author_books as (
    select
        a.id,
        a.name,
        array_agg(distinct b.name order by b.name) as books
    from
        author a
        left outer join book b
            on b.author_id = a.id
    group by
        a.id,
        a.name
    order by
        a.name
);
