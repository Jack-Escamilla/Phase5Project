import React, { useEffect, useState } from "react";


function BookClubs() {
    const [bookClubs, setBookClubs] = useState([]);
    const [newBookClub, setNewBookClub] = useState({ name: '' });
    const [books, setBooks] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetchBookClubs();
        fetchBooks();
    }, []);

    const fetchBookClubs = () => {
        fetch('/api/bookclubs')
            .then(response => response.json())
            .then(data => {
                setBookClubs(data);
            })
            .catch(error => console.error('Error fetching book clubs:', error));
    };
    const fetchBooks = () => {
        fetch('/api/books')
            .then(response => response.json())
            .then(data => {
                setBooks(data.books);
            })
            .catch(error => console.error('Error fetching books:', error));
    };

    const handleSubmitBookClub = () => {
        fetch('/api/save-bookclub', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newBookClub),
        })
            .then(response => response.json())
            .then(data => {
                setBookClubs([...bookClubs, data.bookclub]);
                setNewBookClub({ name: '' });
            })
            .catch(error => console.error('Error creating book club:', error));
    };

    const handleDeleteBookClub = (id) => {
        fetch(`/api/bookclubs/${id}`, {
            method: 'DELETE',
        })
            .then(() => setBookClubs(bookClubs.filter(bc => bc.id !== id)))
            .catch(error => console.error('Error deleting book club:', error));
    };

    const filteredBooks = books.filter(book =>
        book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        book.author.toLowerCase().includes(searchTerm.toLowerCase()) ||
        book.genre.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleAddBookToLibrary = (book) => {
        fetch('/api/librarybooks/<int:library_id>', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(book),
        })
            .then(response => response.json())
            .then(book => {
                setBooks([book.librarys]);
            })
            .catch(error => console.error('Error adding book:', error));
    };

    // const handleChangeName = (id, name) => {
    //     fetch(`/api/bookclubs/${id}`, {
    //         method: 'PUT',
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify({ name }),
    //     })
    //         .then(response => response.json())
    //         .then(data => {
    //             const updatedBookClubs = bookClubs.map(bc => bc.id === id ? data.bookclub : bc);
    //             setBookClubs(updatedBookClubs);
    //         })
    //         .catch(error => console.error('Error updating book club name:', error));
    // };

    return (
        <>
        
            <div>
                <h3>My Book Clubs</h3>
                {bookClubs.length === 0 ? (
                    <p>No book clubs created</p>
                ) : (
                    <ul>
                        {bookClubs.map(bookClub => (
                            <li key={bookClub.id}>
                                <div>
                                    <h4>{bookClub.name}</h4>
                                    <button onClick={() => handleDeleteBookClub(bookClub.id)}>Delete</button>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
                <div>
                    <input type="text" placeholder="Name" value={newBookClub.name} onChange={(e) => setNewBookClub({ ...newBookClub, name: e.target.value })} />
                    <button onClick={handleSubmitBookClub}>Create Book Club</button>
                </div>
            </div>
            <div>
                <h3>Books</h3>
                <input
                    type="text"
                    placeholder="Search..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
                <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
                <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Author</th>
                <th>Genre</th>
                <th>Add To Library</th>
              </tr>
            </thead>
            <tbody>
              {filteredBooks.map((book) => (
                <tr key={book.id}>
                  <td>{book.title}</td>
                  <td>{book.author}</td>
                  <td>{book.genre}</td>
                  <td>
                    <button onClick={() => handleAddBookToLibrary(book.id)}>
                      Add
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
                </div>
            </div>
        </>
    );
}

export default BookClubs;