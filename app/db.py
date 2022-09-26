from sqlalchemy import create_engine


# Establish database databaseection
database = create_engine("postgresql://ratestask:ratestask@db:5432/ratestask")