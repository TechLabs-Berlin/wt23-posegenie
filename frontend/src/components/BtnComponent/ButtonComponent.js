import React from "react";
import "./ButtonComponent.css";

class ButtonComponent extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      activeButton: null,
    };

    this.handleButtonClick = this.handleButtonClick.bind(this);
  }

  handleButtonClick(buttonNumber) {
    // Send a signal to the backend using an HTTP request
    fetch("/backend", {
      method: "POST",
      body: JSON.stringify({ buttonNumber: buttonNumber }),
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => {
        // Handle the response from the backend
        this.setState({ activeButton: buttonNumber });
      })
      .catch((error) => {
        // Handle any errors that occur during the HTTP request
      });
  }

  render() {
    return (
      <div className="container">
        <div>
          <h2>Choose an exercise</h2>
        </div>
        <div className="btn_container">
          <button
            className={this.state.activeButton === 1 ? "active" : ""}
            onClick={() => this.handleButtonClick(1)}
          >
            Lunges
          </button>
          <button
            className={this.state.activeButton === 2 ? "active" : ""}
            onClick={() => this.handleButtonClick(2)}
          >
            Warrior
          </button>
        </div>
      </div>
    );
  }
}

export default ButtonComponent;
