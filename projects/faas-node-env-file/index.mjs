export const handler = async (event) => {
  console.log("Function was called");

  // We build a JSON response with the exact fields the test expects
  const responseBody = {
    status: "success",
    env: {
      TEST_ENV_VAR: process.env["TEST_ENV_VAR"],
      TEST_SECOND_ENV_VAR: process.env["TEST_SECOND_ENV_VAR"],
      SECRET_ENV_VAR: process.env["SECRET_ENV_VAR"],
      CLEARTEXT_ENV_VAR: process.env["CLEARTEXT_ENV_VAR"],
      SECRET_ENV_VAR: process.env["SECRET_ENV_VAR"],
      HELLO_WORLD_FUNCTION_URL: process.env["HELLO_WORLD_FUNCTION_URL"],
      HELLO_WORLD_FUNCTION_NAME: process.env["HELLO_WORLD_FUNCTION_NAME"],
    }
  };

  // Return the response with a 200 status code and the JSON body
  return {
    statusCode: 200,
    body: JSON.stringify(responseBody),
  };
};
