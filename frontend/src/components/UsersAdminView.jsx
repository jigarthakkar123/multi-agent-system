import React, { useState, useEffect } from 'react';
import { Shield, UserCheck, UserX, Trash2, RefreshCw } from 'lucide-react';
import { getUsers, updateUserRole, updateUserStatus, deleteUser } from '../services/api';

export default function UsersAdminView() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchUsers = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await getUsers();
      setUsers(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load user registry. Administrator privileges required.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleRoleChange = async (userId, newRole) => {
    try {
      await updateUserRole(userId, newRole);
      fetchUsers();
    } catch (err) {
      alert('Error updating role: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleStatusToggle = async (userId, currentStatus) => {
    try {
      await updateUserStatus(userId, !currentStatus);
      fetchUsers();
    } catch (err) {
      alert('Error updating status: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm(`Are you sure you want to permanently delete user #${userId}?`)) return;
    try {
      await deleteUser(userId);
      fetchUsers();
    } catch (err) {
      alert('Error deleting user: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="space-y-6">
      <div className="glass-card p-5 rounded-2xl border border-slate-800 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Shield className="w-5 h-5 text-indigo-400" />
            <h2 className="text-base font-bold text-white">Platform User Management & RBAC Governance</h2>
          </div>
          <p className="text-xs text-slate-400">
            Enforce Role-Based Access Control (Admin, Manager, Analyst, Agent) and inspect authentication status.
          </p>
        </div>
        <button
          onClick={fetchUsers}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold bg-slate-900 border border-slate-700 hover:bg-slate-800 text-slate-200"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh</span>
        </button>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-xs text-rose-300">
          {error}
        </div>
      )}

      <div className="glass-card rounded-2xl border border-slate-800 overflow-hidden">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-900/80 text-slate-400 uppercase tracking-wider text-[10px] border-b border-slate-800">
            <tr>
              <th className="p-4">User</th>
              <th className="p-4">Role (RBAC)</th>
              <th className="p-4">Account Status</th>
              <th className="p-4">Registered Date</th>
              <th className="p-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {users.map((u) => (
              <tr key={u.id} className="hover:bg-slate-900/40 transition-colors">
                <td className="p-4">
                  <div className="font-semibold text-white">{u.full_name}</div>
                  <div className="text-[11px] text-slate-400 font-mono">{u.email}</div>
                </td>
                <td className="p-4">
                  <select
                    value={u.role}
                    onChange={(e) => handleRoleChange(u.id, e.target.value)}
                    className="bg-slate-900 border border-slate-700 rounded-lg px-2 py-1 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
                  >
                    <option value="admin">Administrator</option>
                    <option value="manager">Operations Manager</option>
                    <option value="analyst">Data Analyst</option>
                    <option value="agent">Broker Agent</option>
                  </select>
                </td>
                <td className="p-4">
                  {u.is_active ? (
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      <UserCheck className="w-3 h-3" />
                      Active
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">
                      <UserX className="w-3 h-3" />
                      Deactivated
                    </span>
                  )}
                </td>
                <td className="p-4 text-slate-400">
                  {u.created_at ? new Date(u.created_at).toLocaleDateString() : 'Baseline'}
                </td>
                <td className="p-4 text-right">
                  <div className="flex items-center justify-end gap-2">
                    <button
                      onClick={() => handleStatusToggle(u.id, u.is_active)}
                      className="px-2.5 py-1 rounded-lg text-[11px] font-medium bg-slate-800 hover:bg-slate-700 text-slate-300"
                    >
                      {u.is_active ? 'Deactivate' : 'Activate'}
                    </button>
                    <button
                      onClick={() => handleDeleteUser(u.id)}
                      className="p-1 rounded-lg text-rose-400 hover:bg-rose-500/10"
                      title="Delete User"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
