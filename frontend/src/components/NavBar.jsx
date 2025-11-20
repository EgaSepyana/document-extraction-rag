import React from "react";
import logo from "../../src/assets/Logo.svg";

export const NavBar = () => {
  return (
    <nav className="w-full z-50 border-b border-solid dark:border-primary-border-dark fixed top-0 left-0 bg-white dark:bg-bg-dark">
      <div className="py-2 px-20 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <img src={logo} alt="" className="w-8" />
          <h1 className="text-xl font-bold">RAGA</h1>
        </div>
        <div className="flex justify-between items-center gap-5">
          <div className="flex justify-between items-center gap-10 text-sm font-bold">
            <h1>
              <a href="">Help</a>
            </h1>
            <h1>
              <a href="">My Account</a>
            </h1>
          </div>
          <div className="w-10 h-10 bg-primary-base rounded-4xl overflow-hidden">
            <img
              src="https://i.pinimg.com/736x/bd/6f/99/bd6f99210ee96c2d334824352f12e2ff.jpg"
              alt=""
              className="w-full h-full object-cover"
            />
          </div>
        </div>
      </div>
    </nav>
  );
};
