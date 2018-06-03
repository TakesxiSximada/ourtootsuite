db.toots.find({reblog: null})
    .limit(1000)
    .forEach((toot) => {
        print(toot.content);
    });
