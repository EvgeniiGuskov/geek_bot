class DatabaseUpdater:
    def insert_values(self, table, **kwargs):
        record = table(
            **kwargs
        )
        self.session.add(record)
        self.session.commit()
        return record
