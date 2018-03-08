import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import $ from 'jquery'; 

class App extends Component {

  onError(error){
    console.log(error)
  }

  constructor(props) {
    super(props);

    this.state = {
    }

  }

  componentDidMount() {
      this.getData()
  }


  getData(){
    clearTimeout()
    var url = "http://127.0.0.1:5000/"
    $.get(url).then(result => {
        this.setState(JSON.parse(result))
        console.log(result)
      }) 
    setTimeout( this.getData.bind(this), 500)
  }


  onClick(e){
    console.log(e.target.id)
    // console.log(this.state)

    fetch('http://localhost:5000/' + e.target.id + '/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify(this.state),
      success: console.log('success')
    })

      
    
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
            <h1 className="App-title">ClimateChase</h1>
        </header>
        <div style={{'margin-top': '20px'}}>
          year
          <h1>{Math.round(this.state.Curr_Year)}</h1>
          <hr style={{'max-width': 100}} />
          <h4> GDP: ${Math.round(this.state.GDP,3)}B</h4>
          <h4> GHGe: {Math.round(this.state.GHG,3)}kgCO2</h4>
          <h4>Budget: ${Math.round(this.state.Budget,3)}B</h4>
          <p>crop yields: 100% | hurricane strength: 0 | violence: 0 | migration: 0 | sea level: 0</p>
          <hr />
          <p>invest in</p>
        </div>
        <div>
          <div>
            <button class="btn btn-outline-primary" onClick={this.onClick.bind(this)} id="wind">wind</button>
            <button class="btn btn-outline-success" onClick={this.onClick.bind(this)} id="solar">solar</button>
            <button class="btn btn-outline-secondary" onClick={this.onClick.bind(this)} id="nuclear">nuclear</button>
            <button class="btn btn-outline-warning" onClick={this.onClick.bind(this)} id="fossil">fossil</button>
          </div>
        </div>
      
         { this.state.Win ? <h1 style={{'color': 'lightgreen'}}><b>YOU ARE SAFE FROM CLIMATE CHANGE</b></h1> : null }
         { this.state.Game_Over & !this.state.Win ? <h1 style={{'color': 'red'}}><b>YOU LOST TO GLOBAL WARMING</b></h1> : null }
      </div>
    );
  }

  
}

export default App;