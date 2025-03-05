/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(() => {
var exports = {};
exports.id = "pages/_app";
exports.ids = ["pages/_app"];
exports.modules = {

/***/ "./context/AuthContext.tsx":
/*!*********************************!*\
  !*** ./context/AuthContext.tsx ***!
  \*********************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.a(module, async (__webpack_handle_async_dependencies__, __webpack_async_result__) => { try {\n__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   AuthProvider: () => (/* binding */ AuthProvider),\n/* harmony export */   useAuth: () => (/* binding */ useAuth)\n/* harmony export */ });\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-dev-runtime */ \"react/jsx-dev-runtime\");\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ \"react\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! axios */ \"axios\");\n/* harmony import */ var next_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! next/router */ \"./node_modules/next/router.js\");\n/* harmony import */ var next_router__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(next_router__WEBPACK_IMPORTED_MODULE_3__);\nvar __webpack_async_dependencies__ = __webpack_handle_async_dependencies__([axios__WEBPACK_IMPORTED_MODULE_2__]);\naxios__WEBPACK_IMPORTED_MODULE_2__ = (__webpack_async_dependencies__.then ? (await __webpack_async_dependencies__)() : __webpack_async_dependencies__)[0];\n\n\n\n\nconst AuthContext = /*#__PURE__*/ (0,react__WEBPACK_IMPORTED_MODULE_1__.createContext)(undefined);\nconst AuthProvider = ({ children })=>{\n    const [user, setUser] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(null);\n    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(true);\n    const router = (0,next_router__WEBPACK_IMPORTED_MODULE_3__.useRouter)();\n    // Check if user is logged in on initial load\n    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(()=>{\n        const checkAuth = async ()=>{\n            const token = localStorage.getItem(\"token\");\n            if (token) {\n                try {\n                    const response = await axios__WEBPACK_IMPORTED_MODULE_2__[\"default\"].get(\"/api/users/me\", {\n                        headers: {\n                            Authorization: `Bearer ${token}`\n                        }\n                    });\n                    setUser(response.data);\n                } catch (error) {\n                    localStorage.removeItem(\"token\");\n                }\n            }\n            setLoading(false);\n        };\n        checkAuth();\n    }, []);\n    // Set up axios interceptor for token handling\n    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(()=>{\n        // Add a request interceptor to add token to all requests\n        axios__WEBPACK_IMPORTED_MODULE_2__[\"default\"].interceptors.request.use((config)=>{\n            const token = localStorage.getItem(\"token\");\n            if (token) {\n                config.headers.Authorization = `Bearer ${token}`;\n            }\n            return config;\n        }, (error)=>Promise.reject(error));\n    }, []);\n    const login = async (username, password)=>{\n        setLoading(true);\n        try {\n            const formData = new URLSearchParams();\n            formData.append(\"username\", username);\n            formData.append(\"password\", password);\n            const response = await axios__WEBPACK_IMPORTED_MODULE_2__[\"default\"].post(\"/api/auth/token\", formData.toString(), {\n                headers: {\n                    \"Content-Type\": \"application/x-www-form-urlencoded\"\n                }\n            });\n            localStorage.setItem(\"token\", response.data.access_token);\n            // Get user details\n            const userResponse = await axios__WEBPACK_IMPORTED_MODULE_2__[\"default\"].get(\"/api/users/me\", {\n                headers: {\n                    Authorization: `Bearer ${response.data.access_token}`\n                }\n            });\n            setUser(userResponse.data);\n            router.push(\"/library\");\n        } catch (error) {\n            console.error(\"Login error:\", error);\n            throw error;\n        } finally{\n            setLoading(false);\n        }\n    };\n    const register = async (username, email, password, fullName)=>{\n        setLoading(true);\n        try {\n            await axios__WEBPACK_IMPORTED_MODULE_2__[\"default\"].post(\"/api/auth/register\", {\n                username,\n                email,\n                password,\n                full_name: fullName\n            });\n            // Auto login after registration\n            await login(username, password);\n        } catch (error) {\n            console.error(\"Registration error:\", error);\n            throw error;\n        } finally{\n            setLoading(false);\n        }\n    };\n    const logout = ()=>{\n        localStorage.removeItem(\"token\");\n        setUser(null);\n        router.push(\"/login\");\n    };\n    const value = {\n        user,\n        loading,\n        login,\n        register,\n        logout,\n        isAuthenticated: !!user\n    };\n    return /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(AuthContext.Provider, {\n        value: value,\n        children: children\n    }, void 0, false, {\n        fileName: \"/Users/andre/Desktop/portfolio/portfolio/illuminai/src/frontend/context/AuthContext.tsx\",\n        lineNumber: 136,\n        columnNumber: 10\n    }, undefined);\n};\nconst useAuth = ()=>{\n    const context = (0,react__WEBPACK_IMPORTED_MODULE_1__.useContext)(AuthContext);\n    if (context === undefined) {\n        throw new Error(\"useAuth must be used within an AuthProvider\");\n    }\n    return context;\n};\n\n__webpack_async_result__();\n} catch(e) { __webpack_async_result__(e); } });//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,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QUFJLENBQUM7SUFDZDtJQUVBLE1BQU1PLFFBQVE7UUFDWnhDO1FBQ0FFO1FBQ0FvQjtRQUNBYTtRQUNBSTtRQUNBRSxpQkFBaUIsQ0FBQyxDQUFDekM7SUFDckI7SUFFQSxxQkFBTyw4REFBQ0osWUFBWThDLFFBQVE7UUFBQ0YsT0FBT0E7a0JBQVF6Qzs7Ozs7O0FBQzlDLEVBQUU7QUFFSyxNQUFNNEMsVUFBVTtJQUNyQixNQUFNQyxVQUFVckQsaURBQVVBLENBQUNLO0lBQzNCLElBQUlnRCxZQUFZL0MsV0FBVztRQUN6QixNQUFNLElBQUlnRCxNQUFNO0lBQ2xCO0lBQ0EsT0FBT0Q7QUFDVCxFQUFFIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vaWxsdW1pbmFpLWZyb250ZW5kLy4vY29udGV4dC9BdXRoQ29udGV4dC50c3g/ZmRmZiJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QsIHsgY3JlYXRlQ29udGV4dCwgdXNlQ29udGV4dCwgdXNlU3RhdGUsIHVzZUVmZmVjdCwgUmVhY3ROb2RlIH0gZnJvbSAncmVhY3QnO1xuaW1wb3J0IGF4aW9zIGZyb20gJ2F4aW9zJztcbmltcG9ydCB7IHVzZVJvdXRlciB9IGZyb20gJ25leHQvcm91dGVyJztcblxuaW50ZXJmYWNlIFVzZXIge1xuICBpZDogbnVtYmVyO1xuICB1c2VybmFtZTogc3RyaW5nO1xuICBlbWFpbDogc3RyaW5nO1xuICBmdWxsX25hbWU6IHN0cmluZyB8IG51bGw7XG59XG5cbmludGVyZmFjZSBBdXRoQ29udGV4dFR5cGUge1xuICB1c2VyOiBVc2VyIHwgbnVsbDtcbiAgbG9hZGluZzogYm9vbGVhbjtcbiAgbG9naW46ICh1c2VybmFtZTogc3RyaW5nLCBwYXNzd29yZDogc3RyaW5nKSA9PiBQcm9taXNlPHZvaWQ+O1xuICByZWdpc3RlcjogKHVzZXJuYW1lOiBzdHJpbmcsIGVtYWlsOiBzdHJpbmcsIHBhc3N3b3JkOiBzdHJpbmcsIGZ1bGxOYW1lPzogc3RyaW5nKSA9PiBQcm9taXNlPHZvaWQ+O1xuICBsb2dvdXQ6ICgpID0+IHZvaWQ7XG4gIGlzQXV0aGVudGljYXRlZDogYm9vbGVhbjtcbn1cblxuY29uc3QgQXV0aENvbnRleHQgPSBjcmVhdGVDb250ZXh0PEF1dGhDb250ZXh0VHlwZSB8IHVuZGVmaW5lZD4odW5kZWZpbmVkKTtcblxuaW50ZXJmYWNlIEF1dGhQcm92aWRlclByb3BzIHtcbiAgY2hpbGRyZW46IFJlYWN0Tm9kZTtcbn1cblxuZXhwb3J0IGNvbnN0IEF1dGhQcm92aWRlcjogUmVhY3QuRkM8QXV0aFByb3ZpZGVyUHJvcHM+ID0gKHsgY2hpbGRyZW4gfSkgPT4ge1xuICBjb25zdCBbdXNlciwgc2V0VXNlcl0gPSB1c2VTdGF0ZTxVc2VyIHwgbnVsbD4obnVsbCk7XG4gIGNvbnN0IFtsb2FkaW5nLCBzZXRMb2FkaW5nXSA9IHVzZVN0YXRlPGJvb2xlYW4+KHRydWUpO1xuICBjb25zdCByb3V0ZXIgPSB1c2VSb3V0ZXIoKTtcblxuICAvLyBDaGVjayBpZiB1c2VyIGlzIGxvZ2dlZCBpbiBvbiBpbml0aWFsIGxvYWRcbiAgdXNlRWZmZWN0KCgpID0+IHtcbiAgICBjb25zdCBjaGVja0F1dGggPSBhc3luYyAoKSA9PiB7XG4gICAgICBjb25zdCB0b2tlbiA9IGxvY2FsU3RvcmFnZS5nZXRJdGVtKCd0b2tlbicpO1xuICAgICAgaWYgKHRva2VuKSB7XG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgY29uc3QgcmVzcG9uc2UgPSBhd2FpdCBheGlvcy5nZXQoJy9hcGkvdXNlcnMvbWUnLCB7XG4gICAgICAgICAgICBoZWFkZXJzOiB7XG4gICAgICAgICAgICAgIEF1dGhvcml6YXRpb246IGBCZWFyZXIgJHt0b2tlbn1gXG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSk7XG4gICAgICAgICAgc2V0VXNlcihyZXNwb25zZS5kYXRhKTtcbiAgICAgICAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICAgICAgICBsb2NhbFN0b3JhZ2UucmVtb3ZlSXRlbSgndG9rZW4nKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICAgc2V0TG9hZGluZyhmYWxzZSk7XG4gICAgfTtcblxuICAgIGNoZWNrQXV0aCgpO1xuICB9LCBbXSk7XG5cbiAgLy8gU2V0IHVwIGF4aW9zIGludGVyY2VwdG9yIGZvciB0b2tlbiBoYW5kbGluZ1xuICB1c2VFZmZlY3QoKCkgPT4ge1xuICAgIC8vIEFkZCBhIHJlcXVlc3QgaW50ZXJjZXB0b3IgdG8gYWRkIHRva2VuIHRvIGFsbCByZXF1ZXN0c1xuICAgIGF4aW9zLmludGVyY2VwdG9ycy5yZXF1ZXN0LnVzZShcbiAgICAgIChjb25maWcpID0+IHtcbiAgICAgICAgY29uc3QgdG9rZW4gPSBsb2NhbFN0b3JhZ2UuZ2V0SXRlbSgndG9rZW4nKTtcbiAgICAgICAgaWYgKHRva2VuKSB7XG4gICAgICAgICAgY29uZmlnLmhlYWRlcnMuQXV0aG9yaXphdGlvbiA9IGBCZWFyZXIgJHt0b2tlbn1gO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBjb25maWc7XG4gICAgICB9LFxuICAgICAgKGVycm9yKSA9PiBQcm9taXNlLnJlamVjdChlcnJvcilcbiAgICApO1xuICB9LCBbXSk7XG5cbiAgY29uc3QgbG9naW4gPSBhc3luYyAodXNlcm5hbWU6IHN0cmluZywgcGFzc3dvcmQ6IHN0cmluZykgPT4ge1xuICAgIHNldExvYWRpbmcodHJ1ZSk7XG4gICAgdHJ5IHtcbiAgICAgIGNvbnN0IGZvcm1EYXRhID0gbmV3IFVSTFNlYXJjaFBhcmFtcygpO1xuICAgICAgZm9ybURhdGEuYXBwZW5kKCd1c2VybmFtZScsIHVzZXJuYW1lKTtcbiAgICAgIGZvcm1EYXRhLmFwcGVuZCgncGFzc3dvcmQnLCBwYXNzd29yZCk7XG5cbiAgICAgIGNvbnN0IHJlc3BvbnNlID0gYXdhaXQgYXhpb3MucG9zdCgnL2FwaS9hdXRoL3Rva2VuJywgZm9ybURhdGEudG9TdHJpbmcoKSwge1xuICAgICAgICBoZWFkZXJzOiB7XG4gICAgICAgICAgJ0NvbnRlbnQtVHlwZSc6ICdhcHBsaWNhdGlvbi94LXd3dy1mb3JtLXVybGVuY29kZWQnXG4gICAgICAgIH1cbiAgICAgIH0pO1xuXG4gICAgICBsb2NhbFN0b3JhZ2Uuc2V0SXRlbSgndG9rZW4nLCByZXNwb25zZS5kYXRhLmFjY2Vzc190b2tlbik7XG4gICAgICBcbiAgICAgIC8vIEdldCB1c2VyIGRldGFpbHNcbiAgICAgIGNvbnN0IHVzZXJSZXNwb25zZSA9IGF3YWl0IGF4aW9zLmdldCgnL2FwaS91c2Vycy9tZScsIHtcbiAgICAgICAgaGVhZGVyczoge1xuICAgICAgICAgIEF1dGhvcml6YXRpb246IGBCZWFyZXIgJHtyZXNwb25zZS5kYXRhLmFjY2Vzc190b2tlbn1gXG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgICAgXG4gICAgICBzZXRVc2VyKHVzZXJSZXNwb25zZS5kYXRhKTtcbiAgICAgIHJvdXRlci5wdXNoKCcvbGlicmFyeScpO1xuICAgIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgICBjb25zb2xlLmVycm9yKCdMb2dpbiBlcnJvcjonLCBlcnJvcik7XG4gICAgICB0aHJvdyBlcnJvcjtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgc2V0TG9hZGluZyhmYWxzZSk7XG4gICAgfVxuICB9O1xuXG4gIGNvbnN0IHJlZ2lzdGVyID0gYXN5bmMgKHVzZXJuYW1lOiBzdHJpbmcsIGVtYWlsOiBzdHJpbmcsIHBhc3N3b3JkOiBzdHJpbmcsIGZ1bGxOYW1lPzogc3RyaW5nKSA9PiB7XG4gICAgc2V0TG9hZGluZyh0cnVlKTtcbiAgICB0cnkge1xuICAgICAgYXdhaXQgYXhpb3MucG9zdCgnL2FwaS9hdXRoL3JlZ2lzdGVyJywge1xuICAgICAgICB1c2VybmFtZSxcbiAgICAgICAgZW1haWwsXG4gICAgICAgIHBhc3N3b3JkLFxuICAgICAgICBmdWxsX25hbWU6IGZ1bGxOYW1lXG4gICAgICB9KTtcbiAgICAgIFxuICAgICAgLy8gQXV0byBsb2dpbiBhZnRlciByZWdpc3RyYXRpb25cbiAgICAgIGF3YWl0IGxvZ2luKHVzZXJuYW1lLCBwYXNzd29yZCk7XG4gICAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICAgIGNvbnNvbGUuZXJyb3IoJ1JlZ2lzdHJhdGlvbiBlcnJvcjonLCBlcnJvcik7XG4gICAgICB0aHJvdyBlcnJvcjtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgc2V0TG9hZGluZyhmYWxzZSk7XG4gICAgfVxuICB9O1xuXG4gIGNvbnN0IGxvZ291dCA9ICgpID0+IHtcbiAgICBsb2NhbFN0b3JhZ2UucmVtb3ZlSXRlbSgndG9rZW4nKTtcbiAgICBzZXRVc2VyKG51bGwpO1xuICAgIHJvdXRlci5wdXNoKCcvbG9naW4nKTtcbiAgfTtcblxuICBjb25zdCB2YWx1ZSA9IHtcbiAgICB1c2VyLFxuICAgIGxvYWRpbmcsXG4gICAgbG9naW4sXG4gICAgcmVnaXN0ZXIsXG4gICAgbG9nb3V0LFxuICAgIGlzQXV0aGVudGljYXRlZDogISF1c2VyLFxuICB9O1xuXG4gIHJldHVybiA8QXV0aENvbnRleHQuUHJvdmlkZXIgdmFsdWU9e3ZhbHVlfT57Y2hpbGRyZW59PC9BdXRoQ29udGV4dC5Qcm92aWRlcj47XG59O1xuXG5leHBvcnQgY29uc3QgdXNlQXV0aCA9ICgpOiBBdXRoQ29udGV4dFR5cGUgPT4ge1xuICBjb25zdCBjb250ZXh0ID0gdXNlQ29udGV4dChBdXRoQ29udGV4dCk7XG4gIGlmIChjb250ZXh0ID09PSB1bmRlZmluZWQpIHtcbiAgICB0aHJvdyBuZXcgRXJyb3IoJ3VzZUF1dGggbXVzdCBiZSB1c2VkIHdpdGhpbiBhbiBBdXRoUHJvdmlkZXInKTtcbiAgfVxuICByZXR1cm4gY29udGV4dDtcbn07Il0sIm5hbWVzIjpbIlJlYWN0IiwiY3JlYXRlQ29udGV4dCIsInVzZUNvbnRleHQiLCJ1c2VTdGF0ZSIsInVzZUVmZmVjdCIsImF4aW9zIiwidXNlUm91dGVyIiwiQXV0aENvbnRleHQiLCJ1bmRlZmluZWQiLCJBdXRoUHJvdmlkZXIiLCJjaGlsZHJlbiIsInVzZXIiLCJzZXRVc2VyIiwibG9hZGluZyIsInNldExvYWRpbmciLCJyb3V0ZXIiLCJjaGVja0F1dGgiLCJ0b2tlbiIsImxvY2FsU3RvcmFnZSIsImdldEl0ZW0iLCJyZXNwb25zZSIsImdldCIsImhlYWRlcnMiLCJBdXRob3JpemF0aW9uIiwiZGF0YSIsImVycm9yIiwicmVtb3ZlSXRlbSIsImludGVyY2VwdG9ycyIsInJlcXVlc3QiLCJ1c2UiLCJjb25maWciLCJQcm9taXNlIiwicmVqZWN0IiwibG9naW4iLCJ1c2VybmFtZSIsInBhc3N3b3JkIiwiZm9ybURhdGEiLCJVUkxTZWFyY2hQYXJhbXMiLCJhcHBlbmQiLCJwb3N0IiwidG9TdHJpbmciLCJzZXRJdGVtIiwiYWNjZXNzX3Rva2VuIiwidXNlclJlc3BvbnNlIiwicHVzaCIsImNvbnNvbGUiLCJyZWdpc3RlciIsImVtYWlsIiwiZnVsbE5hbWUiLCJmdWxsX25hbWUiLCJsb2dvdXQiLCJ2YWx1ZSIsImlzQXV0aGVudGljYXRlZCIsIlByb3ZpZGVyIiwidXNlQXV0aCIsImNvbnRleHQiLCJFcnJvciJdLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///./context/AuthContext.tsx\n");

/***/ }),

/***/ "./pages/_app.tsx":
/*!************************!*\
  !*** ./pages/_app.tsx ***!
  \************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.a(module, async (__webpack_handle_async_dependencies__, __webpack_async_result__) => { try {\n__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (/* binding */ App)\n/* harmony export */ });\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-dev-runtime */ \"react/jsx-dev-runtime\");\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _styles_globals_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @/styles/globals.css */ \"./styles/globals.css\");\n/* harmony import */ var _styles_globals_css__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_styles_globals_css__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var react_toastify__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-toastify */ \"react-toastify\");\n/* harmony import */ var react_toastify_dist_ReactToastify_css__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react-toastify/dist/ReactToastify.css */ \"./node_modules/react-toastify/dist/ReactToastify.css\");\n/* harmony import */ var react_toastify_dist_ReactToastify_css__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react_toastify_dist_ReactToastify_css__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var _context_AuthContext__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @/context/AuthContext */ \"./context/AuthContext.tsx\");\nvar __webpack_async_dependencies__ = __webpack_handle_async_dependencies__([react_toastify__WEBPACK_IMPORTED_MODULE_2__, _context_AuthContext__WEBPACK_IMPORTED_MODULE_4__]);\n([react_toastify__WEBPACK_IMPORTED_MODULE_2__, _context_AuthContext__WEBPACK_IMPORTED_MODULE_4__] = __webpack_async_dependencies__.then ? (await __webpack_async_dependencies__)() : __webpack_async_dependencies__);\n\n\n\n\n\nfunction App({ Component, pageProps }) {\n    return /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_context_AuthContext__WEBPACK_IMPORTED_MODULE_4__.AuthProvider, {\n        children: [\n            /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(Component, {\n                ...pageProps\n            }, void 0, false, {\n                fileName: \"/Users/andre/Desktop/portfolio/portfolio/illuminai/src/frontend/pages/_app.tsx\",\n                lineNumber: 10,\n                columnNumber: 7\n            }, this),\n            /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(react_toastify__WEBPACK_IMPORTED_MODULE_2__.ToastContainer, {\n                position: \"top-right\",\n                autoClose: 3000\n            }, void 0, false, {\n                fileName: \"/Users/andre/Desktop/portfolio/portfolio/illuminai/src/frontend/pages/_app.tsx\",\n                lineNumber: 11,\n                columnNumber: 7\n            }, this)\n        ]\n    }, void 0, true, {\n        fileName: \"/Users/andre/Desktop/portfolio/portfolio/illuminai/src/frontend/pages/_app.tsx\",\n        lineNumber: 9,\n        columnNumber: 5\n    }, this);\n}\n\n__webpack_async_result__();\n} catch(e) { __webpack_async_result__(e); } });//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiLi9wYWdlcy9fYXBwLnRzeCIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7O0FBQThCO0FBRWtCO0FBQ0Q7QUFDTTtBQUV0QyxTQUFTRSxJQUFJLEVBQUVDLFNBQVMsRUFBRUMsU0FBUyxFQUFZO0lBQzVELHFCQUNFLDhEQUFDSCw4REFBWUE7OzBCQUNYLDhEQUFDRTtnQkFBVyxHQUFHQyxTQUFTOzs7Ozs7MEJBQ3hCLDhEQUFDSiwwREFBY0E7Z0JBQUNLLFVBQVM7Z0JBQVlDLFdBQVc7Ozs7Ozs7Ozs7OztBQUd0RCIsInNvdXJjZXMiOlsid2VicGFjazovL2lsbHVtaW5haS1mcm9udGVuZC8uL3BhZ2VzL19hcHAudHN4PzJmYmUiXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICdAL3N0eWxlcy9nbG9iYWxzLmNzcyc7XG5pbXBvcnQgdHlwZSB7IEFwcFByb3BzIH0gZnJvbSAnbmV4dC9hcHAnO1xuaW1wb3J0IHsgVG9hc3RDb250YWluZXIgfSBmcm9tICdyZWFjdC10b2FzdGlmeSc7XG5pbXBvcnQgJ3JlYWN0LXRvYXN0aWZ5L2Rpc3QvUmVhY3RUb2FzdGlmeS5jc3MnO1xuaW1wb3J0IHsgQXV0aFByb3ZpZGVyIH0gZnJvbSAnQC9jb250ZXh0L0F1dGhDb250ZXh0JztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gQXBwKHsgQ29tcG9uZW50LCBwYWdlUHJvcHMgfTogQXBwUHJvcHMpIHtcbiAgcmV0dXJuIChcbiAgICA8QXV0aFByb3ZpZGVyPlxuICAgICAgPENvbXBvbmVudCB7Li4ucGFnZVByb3BzfSAvPlxuICAgICAgPFRvYXN0Q29udGFpbmVyIHBvc2l0aW9uPVwidG9wLXJpZ2h0XCIgYXV0b0Nsb3NlPXszMDAwfSAvPlxuICAgIDwvQXV0aFByb3ZpZGVyPlxuICApO1xufSJdLCJuYW1lcyI6WyJUb2FzdENvbnRhaW5lciIsIkF1dGhQcm92aWRlciIsIkFwcCIsIkNvbXBvbmVudCIsInBhZ2VQcm9wcyIsInBvc2l0aW9uIiwiYXV0b0Nsb3NlIl0sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///./pages/_app.tsx\n");

/***/ }),

/***/ "./styles/globals.css":
/*!****************************!*\
  !*** ./styles/globals.css ***!
  \****************************/
/***/ (() => {



/***/ }),

/***/ "next/dist/compiled/next-server/pages.runtime.dev.js":
/*!**********************************************************************!*\
  !*** external "next/dist/compiled/next-server/pages.runtime.dev.js" ***!
  \**********************************************************************/
/***/ ((module) => {

"use strict";
module.exports = require("next/dist/compiled/next-server/pages.runtime.dev.js");

/***/ }),

/***/ "react":
/*!************************!*\
  !*** external "react" ***!
  \************************/
/***/ ((module) => {

"use strict";
module.exports = require("react");

/***/ }),

/***/ "react-dom":
/*!****************************!*\
  !*** external "react-dom" ***!
  \****************************/
/***/ ((module) => {

"use strict";
module.exports = require("react-dom");

/***/ }),

/***/ "react/jsx-dev-runtime":
/*!****************************************!*\
  !*** external "react/jsx-dev-runtime" ***!
  \****************************************/
/***/ ((module) => {

"use strict";
module.exports = require("react/jsx-dev-runtime");

/***/ }),

/***/ "react/jsx-runtime":
/*!************************************!*\
  !*** external "react/jsx-runtime" ***!
  \************************************/
/***/ ((module) => {

"use strict";
module.exports = require("react/jsx-runtime");

/***/ }),

/***/ "fs":
/*!*********************!*\
  !*** external "fs" ***!
  \*********************/
/***/ ((module) => {

"use strict";
module.exports = require("fs");

/***/ }),

/***/ "stream":
/*!*************************!*\
  !*** external "stream" ***!
  \*************************/
/***/ ((module) => {

"use strict";
module.exports = require("stream");

/***/ }),

/***/ "zlib":
/*!***********************!*\
  !*** external "zlib" ***!
  \***********************/
/***/ ((module) => {

"use strict";
module.exports = require("zlib");

/***/ }),

/***/ "axios":
/*!************************!*\
  !*** external "axios" ***!
  \************************/
/***/ ((module) => {

"use strict";
module.exports = import("axios");;

/***/ }),

/***/ "react-toastify":
/*!*********************************!*\
  !*** external "react-toastify" ***!
  \*********************************/
/***/ ((module) => {

"use strict";
module.exports = import("react-toastify");;

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../webpack-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = __webpack_require__.X(0, ["vendor-chunks/next","vendor-chunks/@swc","vendor-chunks/react-toastify"], () => (__webpack_exec__("./pages/_app.tsx")));
module.exports = __webpack_exports__;

})();