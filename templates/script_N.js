import React, {useRef} from "https://cdn.skypack.dev/react@17.0.1";
import ReactDOM from "https://cdn.skypack.dev/react-dom@17.0.1";

const App = () => {

    let name = decodeURI(document.URL);
    let sortDatas = [];
    name = name.slice(name.indexOf("=") + 1);
    let socket = io.connect('ws://' + document.domain + ':' + location.port + '/minesweeper', {
        reconnectionDelayMax: 10000,
        query: {
            "cookie": name
        }
    })
    socket.on("total_rank", (revallrank) => {

        let rev_rank = JSON.parse(revallrank);
        let tbody = document.querySelector('tbody');
        let child = tbody.childNodes;
        for (let i = child.length - 1; i >= 0; i--) {
            tbody.removeChild(child[i]);
        }
        /*创建信息数组*/
        let datas = [];
        sortDatas = [];
        let index = [];
        for (let i = 0; i < rev_rank.length; i++) {
            if (rev_rank[i].boomCount === 0)
                rev_rank[i].kd = rev_rank[i].clearCount
            else {
                rev_rank[i].kd = rev_rank[i].clearCount / rev_rank[i].boomCount;
            }
        }

        for (let key = 0; key < rev_rank.length; key++) {
            datas[key] = {
                name: rev_rank[key].username,
                clearCount: rev_rank[key].clearCount,
                boomCount: rev_rank[key].boomCount,
                kd: rev_rank[key].kd
            };
            index[key] = key;
            sortDatas[key] = rev_rank[key].kd;
        }

        for (let m = 0; m < sortDatas.length; m++) {
            for (let n = 0; n < sortDatas.length; n++) {
                if (m !== n && sortDatas[n] < sortDatas[m]) {
                    let tmp = sortDatas[n];
                    sortDatas[n] = sortDatas[m];
                    sortDatas[m] = tmp;
                    let tmp_index = index[n];
                    index[n] = index[m];
                    index[m] = tmp_index;
                }
            }
        }
    })

    const dados = sortDatas;

    return (
        React.createElement("div", {className: "container"},
            React.createElement("div", {className: "topLeadersList"},
                dados.map((leader, index) =>
                    React.createElement("div", {className: "leader", key: leader.id},
                        index + 1 <= 3 &&
                        React.createElement("div", {className: "containerImage"},
                            React.createElement("img", {className: "image", loading: "lazy", src: leader.image}),
                            React.createElement("div", {className: "crown"},
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
                    React.createElement("div", null, "Name"),
                    React.createElement("div", null, "LVL"),
                    React.createElement("div", null, "XP")),
                React.createElement("div", {className: "list"},
                    dados.map((leader, index) => /*#__PURE__*/
                        React.createElement("div", {className: "player", key: leader.id}, /*#__PURE__*/
                            React.createElement("span", null, " ", index + 1), /*#__PURE__*/
                            React.createElement("div", {className: "user"}, /*#__PURE__*/
                                React.createElement("img", {className: "image", src: leader.image}),
                                React.createElement("span", null, " ", leader.name, " ")),
                            React.createElement("span", null, " ", leader.level, " "),
                            React.createElement("span", null, " ", leader.xp, " ")))))));
};

ReactDOM.render( /*#__PURE__*/React.createElement(App, null),
    document.getElementById("root"));