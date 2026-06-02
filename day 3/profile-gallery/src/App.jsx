import Card from "./components/Card"

function App() {
  const profiles = [
    { id:1, name:"Ray", role:"Frontend Developer", age:21, city:"Bangalore" },
    { id:2, name:"Sky", role:"UI Designer", age:25, city:"Delhi" },
    { id:3, name:"Alex", role:"Backend Engineer", age:28, city:"Mumbai" }
  ]
  return (
    <div className="gallery">
      {
      profiles.map((profile) => (
     <Card
      key={profile.id}
      name={profile.name}
      role={profile.role}
      age={profile.age}
      city={profile.city}
     />
     ))
  }

</div>
  )

}

export default App