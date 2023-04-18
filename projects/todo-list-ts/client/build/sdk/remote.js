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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Remote = void 0;
const https_1 = __importDefault(require("https"));
const http_1 = __importDefault(require("http"));
function makeRequest(request, url, agent) {
    return __awaiter(this, void 0, void 0, function* () {
        const data = JSON.stringify(request);
        const hostUrl = new URL(url);
        const options = {
            hostname: hostUrl.hostname,
            path: hostUrl.search ? hostUrl.pathname + hostUrl.search : hostUrl.pathname,
            port: hostUrl.port,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': data.length,
            },
            agent: agent,
        };
        const client = url.includes('https') ? https_1.default : http_1.default;
        return new Promise((resolve, reject) => {
            const req = client.request(options, res => {
                let body = '';
                res.on('data', d => {
                    body += d;
                });
                res.on('end', function () {
                    return __awaiter(this, void 0, void 0, function* () {
                        const response = JSON.parse(body);
                        resolve(response);
                    });
                });
            });
            req.on('error', error => {
                reject(error);
            });
            req.write(data);
            req.end();
        });
    });
}
/**
 * The class through which all request to the Genezio backend will be passed.
 */
class Remote {
    constructor(url) {
        this.url = undefined;
        this.agent = undefined;
        this.url = url;
        const client = url.includes("https") ? https_1.default : http_1.default;
        this.agent = new client.Agent({ keepAlive: true });
    }
    call(method, ...args) {
        return __awaiter(this, void 0, void 0, function* () {
            const requestContent = { "jsonrpc": "2.0", "method": method, "params": args, "id": 3 };
            const response = yield makeRequest(requestContent, this.url, this.agent);
            if (response.error) {
                return response.error.message;
            }
            return response.result;
        });
    }
}
exports.Remote = Remote;
