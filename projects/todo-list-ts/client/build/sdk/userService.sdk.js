"use strict";
/**
* This is an auto generated code. This code should not be modified since the file can be overwriten
* if new genezio commands are executed.
*/
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var _a, _UserService_connect;
Object.defineProperty(exports, "__esModule", { value: true });
exports.Remote = exports.UserService = void 0;
const remote_1 = require("./remote");
Object.defineProperty(exports, "Remote", { enumerable: true, get: function () { return remote_1.Remote; } });
class UserService {
    static register(name, email, password) {
        return __awaiter(this, void 0, void 0, function* () {
            return yield UserService.remote.call("UserService.register", name, email, password);
        });
    }
    static login(email, password) {
        return __awaiter(this, void 0, void 0, function* () {
            return yield UserService.remote.call("UserService.login", email, password);
        });
    }
    static checkSession(token) {
        return __awaiter(this, void 0, void 0, function* () {
            return yield UserService.remote.call("UserService.checkSession", token);
        });
    }
}
exports.UserService = UserService;
_a = UserService, _UserService_connect = function _UserService_connect() {
    return __awaiter(this, void 0, void 0, function* () {
        return yield UserService.remote.call("UserService.#connect");
    });
};
UserService.remote = new remote_1.Remote("http://127.0.0.1:8083/UserService");
