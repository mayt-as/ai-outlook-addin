export const getSSOToken = async (): Promise<string> => {
  return new Promise((resolve, reject) => {
    if (!Office || !Office.context || !Office.context.auth) {
      reject(new Error("Office SSO is not supported in this environment."));
      return;
    }

    Office.context.auth.getAccessTokenAsync(
      { allowSignInPrompt: true, allowConsentPrompt: true, forMSGraphAccess: true },
      (result) => {
        if (result.status === Office.AsyncResultStatus.Succeeded) {
          resolve(result.value);
        } else {
          console.error("SSO Token error:", result.error);
          reject(result.error);
        }
      }
    );
  });
};
