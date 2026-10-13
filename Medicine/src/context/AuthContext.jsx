import { createContext, useEffect, useState } from 'react'

const USERS_KEY = 'medleaf_users'
const SESSION_KEY = 'medleaf_session'

function readUsers() {
  try {
    const raw = localStorage.getItem(USERS_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function saveUsers(users) {
  localStorage.setItem(USERS_KEY, JSON.stringify(users))
}

function readSession() {
  try {
    const raw = localStorage.getItem(SESSION_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

function saveSession(session) {
  if (session) {
    localStorage.setItem(SESSION_KEY, JSON.stringify(session))
  } else {
    localStorage.removeItem(SESSION_KEY)
  }
}

const AuthContext = createContext(null)

function AuthProvider({ children }) {
  const [user, setUser] = useState(() => readSession())

  useEffect(() => {
    if (user) {
      saveSession(user)
    }
  }, [user])

  function register({ name, email, password }) {
    const users = readUsers()
    const normalizedEmail = String(email ?? '').trim().toLowerCase()

    if (!name || !normalizedEmail || !password) {
      return { ok: false, error: 'Please fill in all fields.' }
    }
    if (users.some((u) => u.email === normalizedEmail)) {
      return {
        ok: false,
        error: 'An account with this email already exists. Please sign in.',
      }
    }

    const account = {
      id: `user_${Date.now()}`,
      name: String(name).trim(),
      email: normalizedEmail,
      password,
      createdAt: new Date().toISOString(),
    }
    users.push(account)
    saveUsers(users)

    setUser({
      id: account.id,
      name: account.name,
      email: account.email,
      createdAt: account.createdAt,
    })
    return { ok: true }
  }

  function login({ email, password }) {
    const users = readUsers()
    const normalizedEmail = String(email ?? '').trim().toLowerCase()

    const match = users.find((u) => u.email === normalizedEmail)
    if (!match || match.password !== password) {
      return { ok: false, error: 'Invalid email or password.' }
    }

    setUser({
      id: match.id,
      name: match.name,
      email: match.email,
      createdAt: match.createdAt,
    })
    return { ok: true }
  }

  function logout() {
    setUser(null)
    saveSession(null)
  }

  function resetPassword({ email, password }) {
    const users = readUsers()
    const normalizedEmail = String(email ?? '').trim().toLowerCase()

    const account = users.find((u) => u.email === normalizedEmail)
    if (!account) {
      return { ok: false, error: 'No account found for this email.' }
    }

    account.password = password
    saveUsers(users)
    return { ok: true }
  }

  function getAccount() {
    if (!user) return null
    const users = readUsers()
    return users.find((u) => u.email === user.email) ?? null
  }

  return (
    <AuthContext.Provider
      value={{ user, register, login, logout, resetPassword, getAccount }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export { AuthContext }
export default AuthProvider