import React, { useState, useEffect } from 'react';

function Library() {
  const [library, setLibrary] = useState([]);
  

  useEffect(() => {
    fetchLibrary();
  }, []);

  const fetchLibrary = () => {
    fetch('/api/librarybooks/<int:library_id>')
        .then(response => response.json())
        .then(data => {
            setLibrary(data);
        })
        .catch(error => console.error('Error fetching Library:', error));
  };


  const handleDeleteBook = (bookId) => {
    fetch(`/api/library/${bookId}`, {
      method: 'DELETE',
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to delete book');
        }
        fetchLibrary();
      })
      .catch(error => console.error('Error deleting book:', error));
  };

  return (
    <div>
      <h3>Library</h3>
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>Genre</th>
          </tr>
        </thead>
        <tbody>
          {library.map(book => (
            <tr key={book.id}>
              <td>{book.title}</td>
              <td>{book.author}</td>
              <td>{book.genre}</td>
              <td>
                <button onClick={() => handleDeleteBook(book.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
  );
}

export default Library;