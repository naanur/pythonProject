import React, { Component } from 'react';
import { Route, Routes, BrowserRouter } from 'react-router-dom'
import './App.css';
import ProductsList from "./ProductsList";



const BaseLayout = () => (
  <div className="container-fluid">
<nav className="navbar navbar-expand-lg navbar-light bg-light">
  <a className="navbar-brand" href="/">Django React Test Task</a>
  <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
    <span className="navbar-toggler-icon"></span>
  </button>
  <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
    <div className="navbar-nav">
      <a className="nav-item nav-link" href="/">Main</a>

    </div>
  </div>
</nav>

    <div className="content">

        <Routes>
        <Route path="/" exact component={ProductsList} />
        </Routes>
        <ProductsList />

    </div>


  </div>
)

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <BaseLayout/>
      </BrowserRouter>
    );
  }
}

export default App;