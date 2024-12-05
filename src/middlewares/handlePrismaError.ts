import { PrismaClientKnownRequestError, PrismaClientValidationError } from '@prisma/client/runtime/react-native.js';
import { ErrorRequestHandler } from 'express';
import HttpError from 'http-errors';

// * Middleware for handling all the prisma known errors and validation errors
// * as a BadRequest
const handlePrismaError: ErrorRequestHandler = (error, req, res, next) => {
  if (
    error instanceof PrismaClientKnownRequestError ||
    error instanceof PrismaClientValidationError
  ) {
    return next(new HttpError.BadRequest(error.message));
  }
  return next(error);
};

export default handlePrismaError;
