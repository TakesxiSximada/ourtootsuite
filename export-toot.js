db.toots.find(
    {
        reblog: null,
        visibility: {$ne: "direct"}
    })
    // .limit(10000)
    .forEach((toot) => {
        print(toot.content);
    });
