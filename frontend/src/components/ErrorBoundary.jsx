import React from "react";


export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="page-container">
          <div className="empty-state">
            <h3>Something went wrong</h3>
            <p>Please refresh the page. Your backend records are not affected.</p>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
