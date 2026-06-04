import React from 'react'

export const App = () => {
    function Card(props){
        return (
            <div>
                <h1>{props.name}</h1>
                <p>{props.role}</p>
            </div>
        )
    }
  return (
    <div>App</div>
  )
}

