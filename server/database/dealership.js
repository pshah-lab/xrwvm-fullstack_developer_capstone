const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const dealershipSchema = new Schema(
  {
    id: {
      type: Number,
      required: true,
      unique: true, // Optional but recommended if `id` is meant to be unique
    },
    city: {
      type: String,
      required: true,
    },
    state: {
      type: String,
      required: true,
    },
    address: {
      type: String,
      required: true,
    },
    zip: {
      type: String,
      required: true,
    },
    lat: {
      type: Number,
      required: true,
    },
    long: {
      type: Number,
      required: true,
    },
    short_name: {
      type: String,
    },
    full_name: {
      type: String,
      required: true,
    },
  },
  {
    timestamps: true, // Automatically adds createdAt and updatedAt
  }
);

module.exports = mongoose.model("Dealership", dealershipSchema);
