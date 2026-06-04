import { useState } from "react"

import Card from "./component/Card"

function App() {

  const [profiles, setProfiles] = useState([])
  const [isDark, setIsDark] = useState(false)

  const [name, setName] = useState("")
  const [age, setAge] = useState("")
  const [city, setCity] = useState("")
  const [role, setRole] = useState("")
  function toggleTheme() {
  setIsDark(!isDark)
}
  function addProfile() {

    const newProfile = {

      id: Date.now(),

      name: name,

      age: age,

      city: city,

      role: role

    }

    setProfiles([...profiles, newProfile])

    setName("")
    setAge("")
    setCity("")
    setRole("")

  }

  return (

    <div className={isDark ? "dark" : "light"}>

      <h1 className="heading">Profile Gallery</h1>
      <button onClick={toggleTheme}>
  Toggle Theme
</button>

      <div className="form">

        <input
          type="text"
          placeholder="Enter name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <input
          type="number"
          placeholder="Enter age"
          value={age}
          onChange={(e) => setAge(e.target.value)}
        />

        <input
          type="text"
          placeholder="Enter city"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />

        <input
          type="text"
          placeholder="Enter role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        />

        <button onClick={addProfile}>
          Add Profile
        </button>

      </div>

      <div className="gallery">

        {

          profiles.map((profile) => (

            <Card
              key={profile.id}
              name={profile.name}
              age={profile.age}
              city={profile.city}
              role={profile.role}
            />

          ))

        }

      </div>

    </div>

  )

}

export default App