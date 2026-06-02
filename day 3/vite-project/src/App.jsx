import React from 'react'

const App = () => {
    const a=10
    name = "Kritika"
    const age =21

    const changeUser = () => {
        name = "Kittu"
    }
  return (
    <div>
        <h1>App {a}</h1>
        <div><h2>Hello {name}</h2>
        <h1>age is : {age}</h1>
        <button onClick={changeUser}>Change user</button>
        </div>  
    </div>
  )
}

export default App
