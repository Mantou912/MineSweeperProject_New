import React, {useRef} from "https://cdn.skypack.dev/react@17.0.1";
import ReactDOM from "https://cdn.skypack.dev/react-dom@17.0.1";

const App = () => {
    const dados = [
        {
            id: 1,
            name: 'Laura',
            image: 'imgs/1.jpg',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'imgs/2.jpg',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'imgs/3.jpg',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'imgs/4.jpg',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'https://cdn-icons-png.flaticon.com/512/186/186037.png',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'https://cdn-icons-png.flaticon.com/512/186/186037.png',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'https://cdn-icons-png.flaticon.com/512/186/186037.png',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'https://cdn-icons-png.flaticon.com/512/186/186037.png',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'https://cdn-icons-png.flaticon.com/512/186/186037.png',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'https://cdn-icons-png.flaticon.com/512/186/186037.png',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'https://cdn-icons-png.flaticon.com/512/186/186037.png',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'https://cdn-icons-png.flaticon.com/512/186/186037.png',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'https://cdn-icons-png.flaticon.com/512/186/186037.png',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'https://cdn-icons-png.flaticon.com/512/186/186037.png',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'https://cdn-icons-png.flaticon.com/512/186/186037.png',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'https://cdn-icons-png.flaticon.com/512/186/186037.png',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'https://cdn-icons-png.flaticon.com/512/186/186037.png',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        },

        {
            id: 1,
            name: 'Laura',
            image: 'https://cdn-icons-png.flaticon.com/512/186/186037.png',
            level: 16,
            xp: 100,
            coins: 500,
            love: 6,
            beacons: 2,
            resources: 70
        }];

    return /*#__PURE__*/(
        React.createElement("div", {className: "container"}, /*#__PURE__*/
            React.createElement("div", {className: "topLeadersList"},
                dados.map((leader, index) => /*#__PURE__*/
                    React.createElement("div", {className: "leader", key: leader.id},
                        index + 1 <= 3 && /*#__PURE__*/
                        React.createElement("div", {className: "containerImage"}, /*#__PURE__*/
                            React.createElement("img", {className: "image", loading: "lazy", src: leader.image}), /*#__PURE__*/
                            React.createElement("div", {className: "crown"}, /*#__PURE__*/
                                React.createElement("svg", {
                                        id: "crown1",
                                        fill: "#0f74b5",
                                        "data-name": "Layer 1",
                                        xmlns: "http://www.w3.org/2000/svg",
                                        viewBox: "0 0 100 50"
                                    }, /*#__PURE__*/

                                    React.createElement("polygon", {
                                        className: "cls-1",
                                        points: "12.7 50 87.5 50 100 0 75 25 50 0 25.6 25 0 0 12.7 50"
                                    }))), /*#__PURE__*/
                            React.createElement("div", {className: "leaderName"}, leader.name))))), /*#__PURE__*/
            React.createElement("div", {className: "playerslist"}, /*#__PURE__*/
                React.createElement("div", {className: "table"}, /*#__PURE__*/
                    React.createElement("div", null, "#"), /*#__PURE__*/
                    React.createElement("div", null, "Name"), /*#__PURE__*/
                    React.createElement("div", null, "LVL"), /*#__PURE__*/
                    React.createElement("div", null, "XP"), /*#__PURE__*/
                    React.createElement("div", null, "Coins"), /*#__PURE__*/
                    React.createElement("div", null, "Likes"), /*#__PURE__*/
                    React.createElement("div", null, "Pass"), /*#__PURE__*/
                    React.createElement("div", null, "Resources")), /*#__PURE__*/
                React.createElement("div", {className: "list"},
                    dados.map((leader, index) => /*#__PURE__*/
                        React.createElement("div", {className: "player", key: leader.id}, /*#__PURE__*/
                            React.createElement("span", null, " ", index + 1), /*#__PURE__*/
                            React.createElement("div", {className: "user"}, /*#__PURE__*/
                                React.createElement("img", {className: "image", src: leader.image}), /*#__PURE__*/
                                React.createElement("span", null, " ", leader.name, " ")), /*#__PURE__*/
                            React.createElement("span", null, " ", leader.level, " "), /*#__PURE__*/
                            React.createElement("span", null, " ", leader.xp, " "), /*#__PURE__*/
                            React.createElement("span", null, " ", leader.coins, " "), /*#__PURE__*/
                            React.createElement("span", null, " ", leader.love, " "), /*#__PURE__*/
                            React.createElement("span", null, " ", leader.beacons, " "), /*#__PURE__*/
                            React.createElement("span", null, " ", leader.resources, " ")))))));
};

ReactDOM.render( /*#__PURE__*/React.createElement(App, null),
    document.getElementById("root"));