instructions  = [
    'DROP TABLE IF EXISTS email;',
    """

         CREATE TABLE email (
              id INT AUTO_INCREMENT PRIMARY KEY,
              email TEXT NOT NULL,
              subject TEXT NOT NULL,
              content TEXT NOT NULL
        );
    """
] 