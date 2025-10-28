import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { useAuth } from '../contexts/AuthContext';
import { RegisterData } from '../types';

const industrySchema = yup.object({
  email: yup.string().email('Invalid email').required('Email is required'),
  password: yup.string().min(6, 'Password must be at least 6 characters').required('Password is required'),
  confirmPassword: yup.string().oneOf([yup.ref('password')], 'Passwords must match').required('Confirm password is required'),
  companyName: yup.string().required('Company name is required'),
  gstNumber: yup.string().matches(/^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/, 'Invalid GST number').required('GST number is required'),
  name: yup.string().required('Contact person name is required'),
});

const artisanSchema = yup.object({
  email: yup.string().email('Invalid email').required('Email is required'),
  password: yup.string().min(6, 'Password must be at least 6 characters').required('Password is required'),
  confirmPassword: yup.string().oneOf([yup.ref('password')], 'Passwords must match').required('Confirm password is required'),
  name: yup.string().required('Name is required'),
  location: yup.string().required('Location is required'),
});

interface RegisterFormData extends RegisterData {
  confirmPassword: string;
}

const Register: React.FC = () => {
  const [role, setRole] = useState<'industry' | 'artisan'>('industry');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const { register: registerUser } = useAuth();
  const navigate = useNavigate();

  const schema = role === 'industry' ? industrySchema : artisanSchema;

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<RegisterFormData>({
    resolver: yupResolver(schema),
  });

  const handleRoleChange = (newRole: 'industry' | 'artisan') => {
    setRole(newRole);
    reset();
    setError('');
  };

  const onSubmit = async (data: RegisterFormData) => {
    try {
      setLoading(true);
      setError('');
      
      const { confirmPassword, ...registerData } = data;
      const userData: RegisterData = {
        ...registerData,
        role,
      };

      await registerUser(userData);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="flex justify-center mb-6">
            <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-2xl flex items-center justify-center shadow-lg">
              <span className="text-white font-bold text-xl">EC</span>
            </div>
          </div>
          <h2 className="text-3xl font-bold text-gray-800">Join EcoCycle Connect</h2>
          <p className="mt-2 text-gray-600">Create your account and start making a difference</p>
        </div>

        {/* Registration Form */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          )}

          {/* Role Selection */}
          <div className="mb-6">
            <label className="form-label">I am a:</label>
            <div className="grid grid-cols-2 gap-4 mt-2">
              <button
                type="button"
                onClick={() => handleRoleChange('industry')}
                className={`p-4 rounded-lg border-2 transition-all ${
                  role === 'industry'
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="text-center">
                  <svg className="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                  <span className="font-medium">Industry</span>
                </div>
              </button>
              <button
                type="button"
                onClick={() => handleRoleChange('artisan')}
                className={`p-4 rounded-lg border-2 transition-all ${
                  role === 'artisan'
                    ? 'border-secondary-500 bg-secondary-50 text-secondary-700'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="text-center">
                  <svg className="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4h4a2 2 0 002-2V5z" />
                  </svg>
                  <span className="font-medium">Artisan</span>
                </div>
              </button>
            </div>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Common Fields */}
            <div>
              <label className="form-label">Email Address</label>
              <input
                {...register('email')}
                type="email"
                className="form-input"
                placeholder="Enter your email"
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
              )}
            </div>

            <div>
              <label className="form-label">Password</label>
              <input
                {...register('password')}
                type="password"
                className="form-input"
                placeholder="Create a password"
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
              )}
            </div>

            <div>
              <label className="form-label">Confirm Password</label>
              <input
                {...register('confirmPassword')}
                type="password"
                className="form-input"
                placeholder="Confirm your password"
              />
              {errors.confirmPassword && (
                <p className="mt-1 text-sm text-red-600">{errors.confirmPassword.message}</p>
              )}
            </div>

            {/* Role-specific Fields */}
            {role === 'industry' ? (
              <>
                <div>
                  <label className="form-label">Company Name</label>
                  <input
                    {...register('companyName')}
                    type="text"
                    className="form-input"
                    placeholder="Enter company name"
                  />
                  {errors.companyName && (
                    <p className="mt-1 text-sm text-red-600">{errors.companyName.message}</p>
                  )}
                </div>

                <div>
                  <label className="form-label">GST Number</label>
                  <input
                    {...register('gstNumber')}
                    type="text"
                    className="form-input"
                    placeholder="Enter GST number"
                  />
                  {errors.gstNumber && (
                    <p className="mt-1 text-sm text-red-600">{errors.gstNumber.message}</p>
                  )}
                </div>

                <div>
                  <label className="form-label">Contact Person Name</label>
                  <input
                    {...register('name')}
                    type="text"
                    className="form-input"
                    placeholder="Enter contact person name"
                  />
                  {errors.name && (
                    <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
                  )}
                </div>
              </>
            ) : (
              <>
                <div>
                  <label className="form-label">Full Name</label>
                  <input
                    {...register('name')}
                    type="text"
                    className="form-input"
                    placeholder="Enter your full name"
                  />
                  {errors.name && (
                    <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
                  )}
                </div>

                <div>
                  <label className="form-label">Location</label>
                  <input
                    {...register('location')}
                    type="text"
                    className="form-input"
                    placeholder="Enter your city/location"
                  />
                  {errors.location && (
                    <p className="mt-1 text-sm text-red-600">{errors.location.message}</p>
                  )}
                </div>
              </>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Creating Account...
                </div>
              ) : (
                'Create Account'
              )}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Already have an account?{' '}
              <Link to="/login" className="text-primary-600 hover:text-primary-500 font-medium">
                Sign in here
              </Link>
            </p>
          </div>
        </div>

        {/* Back to About */}
        <div className="text-center">
          <Link
            to="/about"
            className="text-sm text-gray-600 hover:text-gray-800 flex items-center justify-center space-x-1"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            <span>Back to About</span>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Register;